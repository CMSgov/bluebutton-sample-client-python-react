# import datetime

from flask import redirect, request

from cms_bluebutton import BlueButton, AuthorizationToken

from ..data.Database import DBcodeChallenges
from . import app
from ..utils.config_util import get_config_settings
from ..utils.user_util import clear_bb2_data, get_loggedin_user
from ..shared.LoggerFactory import LoggerFactory


"""
This is the location of all the routes, via the port specified in the
config, that allows the front-end to communicate with the server to
retrieve data from Blue Button and Medicare.gov
"""

BENE_DENIED_ACCESS = "access_denied"

# initialize the logger object
myLogger = LoggerFactory.get_logger(log_file=__name__, log_level="DEBUG")
loggedInUser = get_loggedin_user()


#####################################################################
# Test route
#####################################################################
@app.route("/", methods=["GET"])
def verify_port_listening():
    return "Listening on Port 3001 for the Server!"


#####################################################################
# Config util for cms_bluebutton sdk
#####################################################################
def get_bluebutton_sdk_config_from_request(request):
    # Get cms_bluebutton configuration and settings from client request
    my_env = request.args.get("env") or "development"
    my_version = request.args.get("version") or "v2"
    config_settings = get_config_settings(my_env)

    return {
        "base_url": config_settings["bb2BaseUrl"],
        "client_id": config_settings["bb2ClientId"],
        "client_secret": config_settings["bb2ClientSecret"],
        "callback_url": config_settings["bb2CallbackUrl"],
        "version": "1" if my_version == "v1" else "2",
        "environment": "PRODUCTION" if my_env == "production" else "SANDBOX",
    }


#####################################################################
# Authorize routes
#####################################################################


@app.route("/api/authorize/authurl", methods=["GET"])
def get_auth_url():
    bb_sdk_config = get_bluebutton_sdk_config_from_request(request)
    bb = BlueButton(bb_sdk_config)
    auth_data = bb.generate_auth_data()

    # Save auth data in user DB for later use (using state as the key)
    DBcodeChallenges[auth_data["state"]] = auth_data

    return bb.generate_authorize_url(auth_data)


@app.route("/api/authorize/currentAuthToken", methods=["GET"])
def get_current_auth_token():
    return loggedInUser.get("authToken")


@app.route("/api/bluebutton/callback/", methods=["GET"])
def authorization_callback():
    try:
        request_query = request.args

        if request_query.get("error") == BENE_DENIED_ACCESS:
            # clear all saved claims data since the bene denied access
            clear_bb2_data()
            myLogger.error("Beneficiary denied application"
                           " access to their data")
            return redirect("http://localhost:3000")

        # Configure cms_bluebutton class instance
        bb_sdk_config = get_bluebutton_sdk_config_from_request(request)
        bb = BlueButton(bb_sdk_config)

        # Get auth_data saved earlier in user DB (using state as the key)
        auth_data = DBcodeChallenges[request_query.get("state")]

        # this gets the token from Medicare.gov once the 'user' authenticates
        auth_token = bb.get_authorization_token(
            auth_data, request_query.get("code", None),
            request_query.get("state", None)
        )

        """DEVELOPER NOTES:
        * This is where you would most likely place some type of
        * persistence service/functionality to store the token along with
        * the application user identifiers.
        *
        * Here we are however, just updating the loggedInUser we pulled
        * from our MockDb, but we aren't persisting that change
        * back into our mocked DB, normally you would want to do this.
        """

        # Here we are grabbing the mocked 'user' for our application
        # to be able to store the access token for that user thereby linking
        # the 'user' of our sample applicaiton with their Medicare.gov account
        # providing access to their Medicare data to our sample application.
        if auth_token and not auth_token.access_token_expired():
            loggedInUser.update({"authToken": auth_token.get_dict()})

            """ DEVELOPER NOTES:
            * Here we will use the token to get the EoB data for the mocked
            * 'user' of the sample application then to save trips to the BB2
            * API we will store it in the mocked db with the mocked 'user'
            *
            * You could also request data for the Patient endpoint and/or
            * the Coverage endpoint here using similar functionality
            """
            # Get auth_token dict from DB and create auth token class object
            auth_token_dict = loggedInUser.get("authToken")

            # Uncomment the following 3-lines to test token refresh
            # auth_token_dict["expires_at"] = datetime.datetime.now(
            #    datetime.timezone.utc
            # ) - datetime.timedelta(seconds=10)
            auth_token = AuthorizationToken(auth_token_dict)

            # Get EOB FHIR resource data
            eob_ret = bb.get_explaination_of_benefit_data(
                {"params": "", "auth_token": auth_token}
            )

            # Store new access token, if it was refreshed.
            new_auth_token = eob_ret.get("auth_token", None)
            if new_auth_token:
                loggedInUser.update({"authToken": new_auth_token.get_dict()})

            # Get eob data on successful response
            eob_response = eob_ret.get("response", None)
            if eob_response.status_code == 200:
                eob_data = eob_response.json()

                if eob_data.get("entry", None) is not None:
                    loggedInUser["eobData"] = eob_data
                else:
                    # error or malformed bundle,generic error message to client
                    loggedInUser.update(
                        {
                            "eobData": {
                                "message": "Unable to load EOB Data"
                                " - fetch FHIR resource error."
                            }
                        }
                    )
            else:
                # error or malformed bundle,generic error message to client
                loggedInUser.update(
                    {
                        "eobData": {
                            "message": "Unable to load EOB Data"
                            " - response status_code = "
                            + str(eob_response.status_code)
                        }
                    }
                )

        else:
            clear_bb2_data()
            # send generic error message to FE
            loggedInUser.update(
                {
                    "eobData": {
                        "message": "Unable to load EOB Data"
                        " - authorization failed."
                    }
                }
            )

    except BaseException as err:
        """DEVELOPER NOTES:
        * This is where you could also use a data service or other exception
        * handling to display or store the error
        """
        myLogger.error(err)
    """DEVELOPER NOTE:
    * This is a hardcoded redirect, but this should be used from settings
    * stored in a conf file or other mechanism
    """
    return redirect("http://localhost:3000")


######################################################################
# DATA Routes
######################################################################

"""
* DEVELOPER NOTES:
* this function is used directly by the front-end to
* retrieve eob data from the logged in user from within the mocked DB
* This would be replaced by a persistence service layer for whatever
*  DB you would choose to use
"""


@app.route("/api/data/benefit", methods=["GET"])
def get_patient_eob():
    if loggedInUser and loggedInUser.get("eobData"):
        return loggedInUser.get("eobData")
    else:
        return {}
