#bb2Util.py

from .generatePKCE import generateCodeChallenge, generateRandomState
from .userUtil import *
from ..data.Database import *
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

""" DEVELOPER NOTES:
* This is our mocked Data Service layer for both the BB2 API
* as well as for our mocked db Service Layer
* we grouped them together for use of use for the front-end
"""

# this function generates the url to get the authorization token using the information from 
#  the settings from the ENV file, the DB, and the Config file
#  it also will generate the verifier and code challenge used to complete the PCKE authorization
def generateAuthorizeUrl(settings, configSettings):

    BB2_AUTH_URL = configSettings.get('bb2BaseUrl') + '/' + settings.version + '/o/authorize'

    pkceParams = ''
    state = generateRandomState(32)

    if (settings.pkce):
        codeChallenge = generateCodeChallenge()
        pkceParams = '&code_challenge_method=S256' + '&code_challenge=' + codeChallenge.get('codeChallenge')
        DBcodeChallenges[state] = codeChallenge
    return BB2_AUTH_URL +'?client_id=' + configSettings.get('bb2ClientId') +'&redirect_uri=' + configSettings.get('bb2CallbackUrl') +'&state=' + state +'&response_type=code' +pkceParams

# This function is where the application makes a call
# to Blue Button to get an authorization token for the user
# once they have been authenticated via medicare.gov and have allowed
# access to their medicare data to the appllcation
def getAccessToken(code, state, configSettings, settings):
    
    BB2_ACCESS_TOKEN_URL = configSettings.get('bb2BaseUrl')+'/'+settings.version+'/o/token/'
    
    PARAMS = {'client_id':configSettings.get('bb2ClientId'),
                'client_secret':configSettings.get('bb2ClientSecret'),
                'code':code,
                'grant_type':'authorization_code',
                'redirect_url':configSettings.get('bb2CallbackUrl')
            }
    if (settings.pkce and state is not None):
        codeChall = DBcodeChallenges[state]
        PARAMS['code_verifier'] = codeChall.get('verifier')
        PARAMS['code_challenge'] = codeChall.get('codeChallenge')
    
    # ensure that you store the clientid, secret, and all pcke data within the data
    # and provide a header with the content type including the boundary or this call will fail
    mp_encoder = MultipartEncoder(PARAMS)
    myResponse = requests.post(url=BB2_ACCESS_TOKEN_URL,data=mp_encoder,headers={'content-type':mp_encoder.content_type})
    return myResponse

# this function is used to query eob data for the authenticated Medicare.gov
#  user and returned - we are then storing in a mocked DB
def getBenefitData(settings, configsSettings, query, loggedInUser):
    PARAMS = {
        'code':query.get('code'),
        'state':query.get('state')
    }
    BB2_BENEFIT_URL = configsSettings.get('bb2BaseUrl') + '/' + settings.version + '/fhir/ExplanationOfBenefit/'
    myHeader = {'Authorization' : 'Bearer '+loggedInUser.get('authToken').get('access_token')}
    beneResponse = requests.get(url=BB2_BENEFIT_URL,params=PARAMS,headers=myHeader)    
    return beneResponse.text

