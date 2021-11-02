# views.py

from flask import redirect, request
import requests
from ..data.Database import *
from . import app
from ..entities.Settings import Settings
from ..utils.configUtil import getConfigSettings
from ..utils.bb2Util import generateAuthorizeUrl, getAccessToken, getBenefitData
from ..utils.userUtil import getLoggedInUser
from ..shared.LoggerFactory import LoggerFactory
import json

"""
This is the location of all the routes, via the port specified in the config, that allows the 
front-end to communicate with the server to retrieve data from Blue Button and Medicare.gov
"""

# initialize the logger object
myLogger = LoggerFactory.get_logger(log_file=__name__,log_level='DEBUG')
loggedInUser = getLoggedInUser()

#########################################################################################
# Authorize routes
#########################################################################################

@app.route('/api/authorize/authurl',methods=['GET'])
def getAuthUrl():
    """ DEVELOPER NOTE:
    * to utilize the latest security features/best practices
    * it is recommended to utilize pkce
    """
    # get configuration and settings
    myEnv = request.args.get('env') or 'development'
    myVersion = request.args.get('version') or 'v2'
    PKCE = request.args.get('pkce') or True

    settings = Settings(myEnv,myVersion,PKCE)

    configSettings = getConfigSettings(myEnv)
    authUrl = generateAuthorizeUrl(settings, configSettings)
    return authUrl

@app.route('/api/authorize/currentAuthToken',methods=['GET'])
def getCurrentAuthToken():
    return loggedInUser.get('authToken')

@app.route('/api/bluebutton/callback/',methods=['GET'])
def authorizationCallback():
    try:
        requestQuery = request.args
        
        if (requestQuery.get('code') == ''):
            myLogger.error('Response was missing access code!')
        if (DBsettings.pkce and requestQuery.get('state')):
            myLogger.error('State is required when using PKCE')
        
        # get configuration and settings
        myEnv = requestQuery.get('env') or 'development'
        myVersion = requestQuery.get('version') or 'v2'
        PKCE = requestQuery.get('pkce') or True

        settings = Settings(myEnv,myVersion,PKCE)

        configSettings = getConfigSettings(myEnv)

        # this gets the token from Medicare.gov once the 'user' authenticates their Medicare.gov account
        response = getAccessToken(requestQuery.get('code'),requestQuery.get('state'),configSettings=configSettings,settings=settings)
        """DEVELOPER NOTES:
        * This is where you would most likely place some type of
        * persistence service/functionality to store the token along with
        * the application user identifiers
        *
        * Here we are however, just updating the loggedInUser we pulled from our MockDb, but we aren't persisting that change
        * back into our mocked DB, normally you would want to do this
        """
        authToken = json.loads(response.text)

        #Here we are grabbing the mocked 'user' for our application
        # to be able to store the access token for that user
        # thereby linking the 'user' of our sample applicaiton with their Medicare.gov account
        # providing access to their Medicare data to our sample application        
        loggedInUser.update({'authToken':authToken})
        

        """ DEVELOPER NOTES:
        * Here we will use the token to get the EoB data for the mocked 'user' of the sample application
        * then to save trips to the BB2 API we will store it in the mocked db with the mocked 'user'
        *
        * You could also request data for the Patient endpoint and/or the Coverage endpoint here
        * using similar functionality
        """
        eobData = getBenefitData(settings=settings,configsSettings=configSettings,query=requestQuery,loggedInUser=loggedInUser)
        loggedInUser.update({'eobData':json.dumps(eobData)})

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
def getPatientEOB():
    if (loggedInUser.get('eobData') == ''):
        return ''
    else:
        return json.loads(loggedInUser.get('eobData'))