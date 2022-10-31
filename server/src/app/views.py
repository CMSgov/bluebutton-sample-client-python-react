import os
from flask import redirect, request
from ..data.Database import *
from . import app
from ..entities.Settings import Settings
from ..utils.config_util import get_config_settings
from ..utils.bb2_util import generate_authorize_url, get_access_token, get_benefit_data
from ..utils.user_util import clear_bb2_data, get_loggedin_user
from ..shared.LoggerFactory import LoggerFactory

"""
This is the location of all the routes, via the port specified in the config, that allows the 
front-end to communicate with the server to retrieve data from Blue Button and Medicare.gov
"""

BENE_DENIED_ACCESS = 'access_denied'

# initialize the logger object
myLogger = LoggerFactory.get_logger(log_file=__name__,log_level='DEBUG')
loggedInUser = get_loggedin_user()

#########################################################################################
# Test route
#########################################################################################
@app.route('/', methods=['GET'])
def verify_port_listening():
    return 'Listening on Port 3001 for the Server!'

#########################################################################################
# Authorize routes
#########################################################################################

@app.route('/api/authorize/authurl', methods=['GET'])
def get_auth_url():
    """ DEVELOPER NOTE:
    * to utilize the latest security features/best practices
    * it is recommended to utilize pkce
    """
    # get configuration and settings
    my_env = request.args.get('env') or 'development'
    my_version = request.args.get('version') or 'v2'
    PKCE = request.args.get('pkce') or True
    return generate_authorize_url(Settings(my_env, my_version, PKCE), get_config_settings(my_env))

@app.route('/api/authorize/currentAuthToken', methods=['GET'])
def get_current_auth_token():
    return loggedInUser.get('authToken')

@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    try:
        request_query = request.args

        if (request_query.get('error') == BENE_DENIED_ACCESS):
            # clear all saved claims data since the bene has denied access for the application
            clear_bb2_data()
            myLogger.error('Beneficiary denied application access to their data')
            return redirect(get_fe_redirect_url())

        if (request_query.get('code') == ''):
            myLogger.error('Response was missing access code!')
        if (DBsettings.pkce and request_query.get('state')):
            myLogger.error('State is required when using PKCE')
        
        # get configuration and settings
        my_env = request_query.get('env') or 'development'
        my_version = request_query.get('version') or 'v2'
        PKCE = request_query.get('pkce') or True

        settings = Settings(my_env, my_version, PKCE)

        config_settings = get_config_settings(my_env)

        # this gets the token from Medicare.gov once the 'user' authenticates their Medicare.gov account
        auth_token = get_access_token(request_query.get('code'), request_query.get('state'), config_settings=config_settings, settings=settings)
        
        """DEVELOPER NOTES:
        * This is where you would most likely place some type of
        * persistence service/functionality to store the token along with
        * the application user identifiers
        *
        * Here we are however, just updating the loggedInUser we pulled from our MockDb, but we aren't persisting that change
        * back into our mocked DB, normally you would want to do this
        """

        # Here we are grabbing the mocked 'user' for our application
        # to be able to store the access token for that user
        # thereby linking the 'user' of our sample applicaiton with their Medicare.gov account
        # providing access to their Medicare data to our sample application        
        if auth_token and auth_token.get('expires_at') is not None:
            loggedInUser.update({'authToken': auth_token})
            
            """ DEVELOPER NOTES:
            * Here we will use the token to get the EoB data for the mocked 'user' of the sample application
            * then to save trips to the BB2 API we will store it in the mocked db with the mocked 'user'
            *
            * You could also request data for the Patient endpoint and/or the Coverage endpoint here
            * using similar functionality
            """

            eob_data = get_benefit_data(settings=settings,configs_settings=config_settings, query=request_query, logged_in_user=loggedInUser)
            
            if eob_data:
                if eob_data.get('entry', None) is not None:
                    loggedInUser['eobData'] = eob_data
                else:
                    # error or malformed bundle, send generic error message to client
                    loggedInUser.update({'eobData': {'message': 'Unable to load EOB Data - fetch FHIR resource error.'}})
        else:
            clear_bb2_data()
            # send generic error message to FE
            loggedInUser.update({'eobData': {'message': 'Unable to load EOB Data - authorization failed.'}})

    except BaseException as err:
        """DEVELOPER NOTES:
        * This is where you could also use a data service or other exception handling
        * to display or store the error
        """
        myLogger.error(err)
    """DEVELOPER NOTE:
    * This is a hardcoded redirect, but this should be used from settings stored in a conf file
    * or other mechanism
    """
    return redirect(get_fe_redirect_url())

#########################################################################################
# DATA Routes
#########################################################################################

""" 
* DEVELOPER NOTES:
* this function is used directly by the front-end to 
* retrieve eob data from the logged in user from within the mocked DB
* This would be replaced by a persistence service layer for whatever
*  DB you would choose to use
"""
@app.route('/api/data/benefit',methods=['GET'])
def get_patient_eob():
    if loggedInUser and loggedInUser.get('eobData'):
        return loggedInUser.get('eobData')
    else:
        return {}


def get_fe_redirect_url():
    is_selenium_tests = os.getenv('SELENIUM_TESTS', 'False').lower() in ('true')
    return 'http://client:3000' if is_selenium_tests else 'http://localhost:3000'
