# views.py
import json

from flask import redirect, request
from ..data.Database import *
from . import app
from ..entities.Settings import Settings
from ..utils.configUtil import get_config_settings
from ..utils.bb2Util import generate_authorize_url, get_access_token, get_benefit_data
from ..utils.userUtil import getLoggedInUser
from ..shared.LoggerFactory import LoggerFactory

"""
This is the location of all the routes, via the port specified in the config, that allows the 
front-end to communicate with the server to retrieve data from Blue Button and Medicare.gov
"""

# initialize the logger object
myLogger = LoggerFactory.get_logger(log_file=__name__,log_level='DEBUG')
loggedInUser = getLoggedInUser()

#########################################################################################
# Test route
#########################################################################################
@app.route('/',methods=['GET'])
def verify_port_listening():
    return 'Listening on Port 3001 for the Server!'

#########################################################################################
# Authorize routes
#########################################################################################

@app.route('/api/authorize/authurl',methods=['GET'])
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

@app.route('/api/authorize/currentAuthToken',methods=['GET'])
def get_current_auth_token():
    return loggedInUser.get('authToken')

@app.route('/api/bluebutton/callback/',methods=['GET'])
def authorization_callback():
    try:
        request_query = request.args
        
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
        response = get_access_token(request_query.get('code'), request_query.get('state'), config_settings=config_settings, settings=settings)
        
        """DEVELOPER NOTES:
        * This is where you would most likely place some type of
        * persistence service/functionality to store the token along with
        * the application user identifiers
        *
        * Here we are however, just updating the loggedInUser we pulled from our MockDb, but we aren't persisting that change
        * back into our mocked DB, normally you would want to do this
        """
        auth_token = json.loads(response.text)
        
        #Here we are grabbing the mocked 'user' for our application
        # to be able to store the access token for that user
        # thereby linking the 'user' of our sample applicaiton with their Medicare.gov account
        # providing access to their Medicare data to our sample application        
        loggedInUser.update({'authToken': auth_token})
        
        """ DEVELOPER NOTES:
        * Here we will use the token to get the EoB data for the mocked 'user' of the sample application
        * then to save trips to the BB2 API we will store it in the mocked db with the mocked 'user'
        *
        * You could also request data for the Patient endpoint and/or the Coverage endpoint here
        * using similar functionality
        """
        eob_data = get_benefit_data(settings=settings,configs_settings=config_settings, query=request_query, logged_in_user=loggedInUser)
        
        if (eob_data != None and eob_data != ''):
            loggedInUser.update({'eobData':json.dumps(eob_data)})
        else:
            loggedInUser.update({'eobData':json.dumps('Unable to load EOB Data!')})

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
    return redirect('http://localhost:3000')

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
    if (loggedInUser != None 
        and loggedInUser.get('eobData') != None
        and loggedInUser.get('eobData') != ''):
        return json.loads(loggedInUser.get('eobData'))
    else:
        return ''