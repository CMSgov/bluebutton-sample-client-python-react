import os
import json

from flask import redirect, request, Flask
from cms_bluebutton.cms_bluebutton import BlueButton


BENE_DENIED_ACCESS = "access_denied"
FE_MSG_ACCESS_DENIED = "Beneficiary denied app access to their data"
ERR_QUERY_EOB = "Error when querying the patient's EOB!"
ERR_MISSING_AUTH_CODE = "Response was missing access code!"
ERR_MISSING_STATE = "State is required when using PKCE"

app = Flask(__name__)
bb = BlueButton()

# This is where medicare.gov beneficiary associated
# with the current logged in app user,
# in real app, this could be the app specific
# account management system
logged_in_user = {
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

    if (request_query.get('error') == BENE_DENIED_ACCESS):
        # clear all cached claims eob data since the bene has denied access
        # for the application
        clear_bb2_data()
        logged_in_user.update({'eobData': {'message': FE_MSG_ACCESS_DENIED}})
        print(FE_MSG_ACCESS_DENIED)
        return redirect(get_fe_redirect_url())

    code = request_query.get('code')

    if code is None:
        print(ERR_MISSING_AUTH_CODE)
        return redirect(get_fe_redirect_url())

    state = request_query.get('state')

    if state is None:
        print(ERR_MISSING_STATE)
        return redirect(get_fe_redirect_url())

    auth_token = bb.get_authorization_token(auth_data, code, state)

    # correlate app user with medicare bene
    logged_in_user['authToken'] = auth_token

    config = {
        "auth_token": auth_token,
        "params": {},
        "url": "to be overriden"
    }

    try:
        # search eob (or other fhir resources: patient, coverage, etc.)
        eob_data = bb.get_explaination_of_benefit_data(config)
        coverage_data = bb.get_c4dic_coverage_data(config)
        patient_data = bb.get_c4dic_patient_data(config)
        org_data = bb.get_c4dic_organization_data(config)

        # fhir search response could contain large number of resources,
        # by default they are chunked into pages of 10 resources each,
        # the response above might be the 1st page of EOBs, it is in
        # the format of a FHIR bundle resource with a link section where
        # page navigation urls such as 'first', 'last', 'self', 'next',
        # 'previous' might present depending on the current page.
        # Use bb.get_pages(data, config) to get all the pages

        auth_token = eob_data['auth_token']
        logged_in_user['authToken'] = auth_token
        logged_in_user['eobData'] = eob_data['response'].json()
        coverage_json = coverage_data['response'].json()
        logged_in_user['coverageData'] = json.dumps(coverage_json, indent=3)
        mbi_plain = coverage_json[0]['subscriberId']
        mbi = "{0}-{1}-{2}".format(mbi_plain[:4], mbi_plain[4:7], mbi_plain[7:])
        coverage = {'mbi': mbi}
        patient_json = patient_data['response'].json()
        org_json = org_data['response'].json()
        coverage['patient_name'] = "{0} {1}".format(patient_json['name'][0]['given'][0], patient_json['name'][0]['family'])
        coverage['organization_name'] = "{0}".format(org_json[0]['name'])
        coverage['organization_active'] = "{0}".format(org_json[0]['active'])
        coverage['date_a'] = coverage_json[0]['period']
        coverage['type'] = coverage_json[0]['type']['coding'][0]['code']
        coverage['plan'] = "Part A, Part B"
        coverage['group'] = "Medicare"
        logged_in_user['coverage'] = coverage
    except Exception as ex:
        clear_bb2_data()
        logged_in_user.update({'eobData': {'message': ERR_QUERY_EOB}})
        print(ERR_QUERY_EOB)
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
    if logged_in_user and logged_in_user.get('eobData'):
        return logged_in_user.get('eobData')
    else:
        return {}


@app.route('/api/data/insurance', methods=['GET'])
def get_insurance():
    """
    * this function is used directly by the front-end to
    * retrieve eob data from the logged in user from within the mocked DB
    * This would be replaced by a persistence service layer for whatever
    *  DB you would choose to use
    """
    if logged_in_user and logged_in_user.get('coverage'):
        return logged_in_user.get('coverage')
    else:
        return {}


@app.route('/api/data/coverage', methods=['GET'])
def get_coverage():
    """
    * this function is used directly by the front-end to
    * retrieve eob data from the logged in user from within the mocked DB
    * This would be replaced by a persistence service layer for whatever
    *  DB you would choose to use
    """
    if logged_in_user and logged_in_user.get('coverageData'):
        return logged_in_user.get('coverageData')
    else:
        return {}


def get_fe_redirect_url():
    '''
    helper to figure out the correct front end redirect url per context
    '''
    is_selenium = os.getenv('SELENIUM_TESTS', 'False').lower() in ('true')
    return 'http://localhost:3000' if is_selenium else 'http://localhost:3000'


def clear_bb2_data():
    '''
    helper to clean up cached result
    '''
    logged_in_user.update({'authToken': None})
    logged_in_user.update({'eobData': {}})
    logged_in_user.update({'coverage': {}})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
