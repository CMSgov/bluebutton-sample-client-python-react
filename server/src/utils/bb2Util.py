import datetime
import re
import requests
import time
import urllib

from .generatePKCE import generateCodeChallenge, generateRandomState
from .userUtil import *
from ..data.Database import *
from requests_toolbelt.multipart.encoder import MultipartEncoder

""" DEVELOPER NOTES:
* This is our mocked Data Service layer for both the BB2 API
* as well as for our mocked db Service Layer
* we grouped them together for use of use for the front-end
"""

# retry interval 5 seconds
RETRY_INTERVAL = 5
# retry max 3
RETRY_MAX = 3

# this function generates the url to get the authorization token using the information from 
#  the settings from the ENV file, the DB, and the Config file
#  it also will generate the verifier and code challenge used to complete the PCKE authorization
def generate_authorize_url(settings, config_settings):

    BB2_AUTH_URL = config_settings.get('bb2BaseUrl') + '/' + settings.version + '/o/authorize'
    state = generateRandomState(32)
    
    PARAMS = {'client_id' : config_settings.get('bb2ClientId'), 'redirect_uri' : config_settings.get('bb2CallbackUrl'), 'state' : state, 'response_type' : 'code'}
    
    if (settings.pkce):
        code_challenge = generateCodeChallenge()
        PARAMS['code_challenge_method'] = 'S256'
        PARAMS['code_challenge'] = code_challenge.get('codeChallenge')
        DBcodeChallenges[state] = code_challenge
    return BB2_AUTH_URL+'?'+urllib.parse.urlencode(PARAMS, quote_via=urllib.parse.quote)

# This function is where the application makes a call
# to Blue Button to get an authorization token for the user
# once they have been authenticated via medicare.gov and have allowed
# access to their medicare data to the appllcation
def get_access_token(code, state, config_settings, settings):
    BB2_ACCESS_TOKEN_URL = config_settings.get('bb2BaseUrl')+'/'+settings.version+'/o/token/'
    PARAMS = {'client_id':config_settings.get('bb2ClientId'),
                'client_secret':config_settings.get('bb2ClientSecret'),
                'code':code,
                'grant_type':'authorization_code',
                'redirect_uri':config_settings.get('bb2CallbackUrl')
            }
    if (settings.pkce and state is not None):
        code_chall = DBcodeChallenges[state]
        PARAMS['code_verifier'] = code_chall.get('verifier')
        PARAMS['code_challenge'] = code_chall.get('codeChallenge')
    
    # ensure that you store the clientid, secret, and all pcke data within the data
    # and provide a header with the content type including the boundary or this call will fail
    mp_encoder = MultipartEncoder(PARAMS)
    my_response = requests.post(url=BB2_ACCESS_TOKEN_URL, data=mp_encoder, headers={'content-type':mp_encoder.content_type})
    check_and_report_error(my_response)
    response_json = my_response.json()
    response_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in'])
    return response_json

def refresh_accesstoken(refresh_token, config_settings, settings):
    BB2_ACCESS_TOKEN_URL = config_settings.get('bb2BaseUrl')+'/'+settings.version+'/o/token/'
    params = {
        'client_id': config_settings.get('bb2ClientId'),
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    my_response = requests.post(url=BB2_ACCESS_TOKEN_URL, params=params, auth=(config_settings.get('bb2ClientId'), config_settings.get('bb2ClientSecret')))
    response_json = my_response.json()
    response_json['expires_at'] = datetime.datetime.now() + datetime.timedelta(seconds=response_json['expires_in'])
    return response_json

# this function is used to query eob data for the authenticated Medicare.gov
# user and returned - we are then storing in a mocked DB
def get_benefit_data(settings, configs_settings, query, logged_in_user):
    if (datetime.datetime.now() > logged_in_user.get('authToken').get('expires_at')):
        updated_auth_token = refresh_accesstoken(logged_in_user.get('authToken').get('refresh_token'), configs_settings, settings)
        logged_in_user.update({'authToken':updated_auth_token})

    PARAMS = {
        'code':query.get('code'),
        'state':query.get('state')
    }

    BB2_BENEFIT_URL = configs_settings.get('bb2BaseUrl') + '/' + settings.version + '/fhir/ExplanationOfBenefit/'
    my_header = {'Authorization' : 'Bearer ' + logged_in_user.get('authToken').get('access_token')}
    bene_response = requests.get(url=BB2_BENEFIT_URL,params=PARAMS,headers=my_header)
    result = retry_and_report_on_error(bene_response, BB2_BENEFIT_URL, PARAMS, my_header)

    return result.json()

def check_and_report_error(response):
    if response.status_code != 200:
        _print_console("Response status code: {}".format(response.status_code))
        _print_console("Response text: {}".format(response.text))

def retry_and_report_on_error(response, url, params, header):
    retry_result = None
    if response.status_code != 200:
        check_and_report_error(response)
        if is_retryable(response):
            retry_result = do_retry(url, params, header)
    return retry_result if retry_result is not None else response

def is_retryable(response):
    return response.status_code == 500 and re.match("^/v[12]/fhir/.*", response.request.path_url)

# for demo: retry init-interval = 5 sec, max attempt 3, with retry interval = init-interval * (2 ** n)
# where n retry attempted
def do_retry(url, params, headers):
    response = None
    _print_console("retrying started ...")
    for i in range(RETRY_MAX):
        wait_in_sec = RETRY_INTERVAL * (2 ** i)
        time.sleep(wait_in_sec)
        _print_console("retry attempts: {}".format(i+1))
        try:
            response = requests.get(url=url, params=params, headers=headers)
            if response.status_code == 200:
                # developer notes: the response can be persisted associated with the bene
                _print_console("retry successful:")
                break
            elif is_retryable(response):
                response = None
                continue
            else:
                # break out on un retryable response
                response = None
                break
        except Exception as e:
            _print_console("retry exception: [{}]".format(e))
            response = None
            break;
    return response

def _print_console(str):
    print(str, flush=True)