import os

from flask import redirect, request, Flask
from cms_bluebutton.cms_bluebutton import BlueButton


app = Flask(__name__)
bb = BlueButton()

# This is where medicare.gov beneficiary associated
# with the current logged in app user,
# in real app, this could be the app specific
# accoount management system
loggedInUser = {
    'authToken': None,
    'eobData': None
}

auth_data = bb.generate_auth_data()

# AuthorizationToken holds access grant info:
# access token, expire in, expire at, token type, scope, refreh token, etc.
# it is associated with current logged in user in real app,
# check SDK python docs for more details.

auth_token = None


@app.route('/api/authorize/authurl', methods=['GET'])
def get_auth_url():
    redirect_url = bb.generate_authorize_url(auth_data)
    return redirect_url


@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    code = request_query.get('code')
    state = request_query.get('state')

    auth_token = bb.get_authorization_token(auth_data, code, state)

    # correlate app user with medicare bene
    loggedInUser['authToken'] = auth_token

    config = {
        "auth_token": auth_token,
        "params": {},
        "url": "to be overriden"
    }

    # result = {}

    try:
        # search eob

        eob_data = bb.get_explaination_of_benefit_data(config)

        # fhir search response could contain large number of resources,
        # by default they are chunked into pages of 10 resources each,
        # the response above might be the 1st page of EOBs, it is in
        # the format of a FHIR bundle resource with a link section where
        # page navigation urls such as 'first', 'last', 'self', 'next',
        # 'previous' might present depending on the current page.
        # Use bb.get_pages(data, config) to get all the pages

        auth_token = eob_data['auth_token']
        loggedInUser['authToken'] = auth_token
        loggedInUser['eobData'] = eob_data['response'].json()
    except Exception as ex:
        print(ex)

    return redirect(get_fe_redirect_url())


@app.route('/api/data/benefit', methods=['GET'])
def get_patient_eob():
    """
    * this function is used directly by the front-end to
    * retrieve eob data from the logged in user from within the mocked DB
    * This would be replaced by a persistence service layer for whatever
    *  DB you would choose to use
    """
    if loggedInUser and loggedInUser.get('eobData'):
        return loggedInUser.get('eobData')
    else:
        return {}


def get_fe_redirect_url():
    '''
    helper to figure out the correct front end redirect url per context
    '''
    is_selenium = os.getenv('SELENIUM_TESTS', 'False').lower() in ('true')
    return 'http://client:3000' if is_selenium else 'http://localhost:3000'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
