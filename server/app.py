import os

from flask import redirect, request, Flask
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse as ext_parse
from cms_bluebutton.cms_bluebutton import BlueButton

BENE_DENIED_ACCESS = "access_denied"
FE_MSG_ACCESS_DENIED = "Beneficiary denied app access to their data"
ERR_QUERY_DATA = "Error when querying the patient's Data: EOB or Coverage or Patient!"
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
        auth_token = eob_data['auth_token']
        coverage_data = bb.get_coverage_data(config)
        auth_token = coverage_data['auth_token']
        patient_data = bb.get_patient_data(config)
        auth_token = patient_data['auth_token']

        config_clone = dict(config)
        config_clone['url'] = "https://test.bluebutton.cms.gov/v2/fhir/Patient?_profile=http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Patient"
        dic_pt_data = bb.get_custom_data(config_clone)
        auth_token = dic_pt_data['auth_token']

        config_clone['url'] = "https://test.bluebutton.cms.gov/v2/fhir/Coverage?_profile=http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Coverage"
        dic_coverage_data = bb.get_custom_data(config_clone)
        auth_token = dic_coverage_data['auth_token']

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
        logged_in_user['coverageData'] = coverage_data['response'].json()
        logged_in_user['patientData'] = patient_data['response'].json()
        logged_in_user['dicPatientData'] = dic_pt_data['response'].json()
        logged_in_user['dicCoverageData'] = dic_coverage_data['response'].json()
    except Exception as ex:
        clear_bb2_data()
        logged_in_user.update({'eobData': {'message': ERR_QUERY_DATA}})
        print(ERR_QUERY_DATA)
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
def get_patient_insurance():
    """
    * This function is used directly by the front-end to
    * retrieve insurance data from the logged in user from within the mocked DB
    * This would be replaced by a persistence service layer for whatever
    *  DB you would choose to use
    *
    * This is for POC, the insurance data composition will be implemented
    * in BB2 server tier, and exposed as an API end point
    """

    ## jsonPath("$.error[?(@.errorMessage=='Fixed Error Message')]").exists
    dic_patient = logged_in_user.get('dicPatientData')
    dic_coverage = logged_in_user.get('dicCoverageData')
    insurance = {}
    if logged_in_user and dic_patient and dic_coverage:
        ## extract info from C4DIC Patient and Coverage
        ## and composite into insurance info and response to
        ## FE for insurance card rendering
        ## Note, Coverage could be paged, not iterate page here for POC purpose

        ## From C4DIC Patient extract:
        ## 1. identifier mbi, e.g. 1S00EU7JH47
        ## 2. name, e.g. Johnie C
        ## 3. gender, e.g. male
        ## 4. dob, e.g. 1990-08-14
        ## From C4DIC Coverage extract:
        ## 1. coverage class: by Coverage resource 'class': "Part A"
        ## 2. status: active or not active
        ## 3. period, start date: e.g. 2014-02-06
        ## 4. relationship to insured: e.g. self
        ## 5. payor: CMS
        ## 6. contract number: e.g. Part D , Part C: ptc_cntrct_id_01...12
        ## 7. reference year: e.g. Part A: 2025, Part B: 2025, etc.
        ## 8. other info such as: DIB, ESRD etc. can be added as needed
        pt = dic_patient['entry']
        patient = pt[0]
        pt_id = lookup_1_and_get("$.resource.identifier[?(@.system=='http://hl7.org/fhir/sid/us-mbi')]", "value", patient)
        insurance['identifier'] = pt_id
        pt_name = patient['resource']['name'][0]['family']
        insurance['name'] = pt_name
        pt_gender = patient['resource']['gender']
        insurance['gender'] = pt_gender
        pt_dob = patient['resource']['birthDate']
        insurance['dob'] = pt_dob

        coverage_array = dic_coverage['entry']
        coverages = {}
        for c in coverage_array:
            c_clazz = lookup_1_and_get("$.resource.class[?(@.type.coding=='plan')]", "value", c)
            coverages['clazz'] = c_clazz if c_clazz else "Null"
            c_status = c['resource']['status']
            coverages['status'] = c_status
            c_start = c['resource']['period']['start']
            coverages['startDate'] = c_start
            c_end = c['resource']['period'].get('end')
            coverages['endDate'] = c_end
            c_payer = c['resource']['payor'][0]
            if c_payer:
                c_payer = c_payer['identifier']['value']
            coverages['payer'] = c_payer
            c_contract_id = "NA" ## Part A and Part B does not have contract number
            if c_clazz == "Part C":
                c_contract_id = lookup_1_and_get("$.resource.extension[?(@.url=='https://bluebutton.cms.gov/resources/variables/ptc_cntrct_id_01')]", "valueCoding", c).get('code')
            if c_clazz == "Part D":
                c_contract_id = lookup_1_and_get("$.resource.extension[?(@.url=='https://bluebutton.cms.gov/resources/variables/ptdcntrct01')]", "valueCoding", c).get('code')
            coverages['contractId'] = c_contract_id
            c_reference_year = jsonpath.query("$.resource.extension[?(@.url=='https://bluebutton.cms.gov/resources/variables/rfrnc_yr')]", c).get('valueDate')
            coverages['referenceYear'] = c_reference_year
            c_relationship = c['resource']['relationship']['coding'][0]['display']
            coverages['relationship'] = c_relationship

        insurance['coverages'] = coverages

    return insurance


def get_fe_redirect_url():
    '''
    helper to figure out the correct front end redirect url per context
    '''
    is_selenium = os.getenv('SELENIUM_TESTS', 'False').lower() in ('true')
    return 'http://client:3000' if is_selenium else 'http://localhost:3000'


def clear_bb2_data():
    '''
    helper to clean up cached result
    '''
    logged_in_user.update({'authToken': None})
    logged_in_user.update({'eobData': {}})
    logged_in_user.update({'coverageData': {}})
    logged_in_user.update({'patientData': {}})
    logged_in_user.update({'dicPatientData': {}})
    logged_in_user.update({'dicCoverageData': {}})


def lookup_by_path(expr, json_obj):
    jsonpath_expr = ext_parse(expr)
    return jsonpath_expr.find(json_obj)
    

def lookup_1_and_get(expr, attribute, json_obj):
    r = lookup_by_path(expr, json_obj)
    if r and isinstance(r, list):
        return r[0].value[attribute]
        

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
