import os
import json

from flask import redirect, request, Flask
from jsonpath_ng import jsonpath
from jsonpath_ng.ext import parse as ext_parse
from cms_bluebutton.cms_bluebutton import BlueButton
from datetime import datetime

C4DIC_COLOR_PALETTE_EXT = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-ColorPalette-extension"
C4DIC_COLOR_BG = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-BackgroundColor-extension"
C4DIC_COLOR_FG = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-ForegroundColor-extension"
C4DIC_COLOR_HI_LT = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-HighlightColor-extension"

C4DIC_LOGO_EXT = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Logo-extension"
C4DIC_ADDL_CARD_INFO_EXT = "http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-AdditionalCardInformation-extension"
CMS_VAR_PTC_CNTRCT_ID_01 = "https://bluebutton.cms.gov/resources/variables/ptc_cntrct_id_01"
CMS_VAR_PTD_CNTRCT_ID_01 = "https://bluebutton.cms.gov/resources/variables/ptdcntrct01"
CMS_VAR_REF_YR="https://bluebutton.cms.gov/resources/variables/rfrnc_yr"

BENE_DENIED_ACCESS = "access_denied"
FE_MSG_ACCESS_DENIED = "Beneficiary denied app access to their data"
ERR_QUERY_DATA = "Error when querying the patient's Data: EOB or Coverage or Patient!"
ERR_MISSING_AUTH_CODE = "Response was missing access code!"
ERR_MISSING_STATE = "State is required when using PKCE"

## helper trouble shoot
def print_setting():
    print(f"URL::BlueButton->base_url: {bb.base_url}", flush=True)
    print(f"URL::BlueButton->auth_base_url: {bb.auth_base_url}", flush=True)
    print(f"URL::BlueButton->auth_token_url: {bb.auth_token_url}", flush=True)
    print(f"URL::BlueButton->callback_url: {bb.callback_url}", flush=True)


app = Flask(__name__)
bb = BlueButton()

host_ip = os.environ.get("HOST_IP")

print_setting()

if host_ip:
    if str(bb.base_url).startswith("http://localhost"):
        bb.base_url = str(bb.base_url).replace("http://localhost", f"http://{host_ip}")
    if str(bb.auth_base_url).startswith("http://localhost"):
        bb.auth_base_url = str(bb.auth_base_url).replace(f"http://localhost", f"http://{host_ip}")
    if str(bb.auth_token_url).startswith("http://localhost"):
        bb.auth_token_url = str(bb.auth_token_url).replace(f"http://localhost", f"http://{host_ip}")
    print_setting()

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
    print_setting()
    redirect_url = bb.generate_authorize_url(auth_data)
    return redirect_url


@app.route('/api/bluebutton/callback/', methods=['GET'])
def authorization_callback():
    request_query = request.args
    print_setting()

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
        config_clone['url'] = f"{bb.base_url}/v2/fhir/Patient?_profile=http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Patient"
        dic_pt_data = bb.get_custom_data(config_clone)
        auth_token = dic_pt_data['auth_token']

        config_clone['url'] = f"{bb.base_url}/v2/fhir/Coverage?_profile=http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Coverage"
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
        ## print(json.dumps(logged_in_user['coverageData']), flush=True)
        logged_in_user['patientData'] = patient_data['response'].json()
        logged_in_user['dicPatientData'] = dic_pt_data['response'].json()
        ## print(json.dumps(logged_in_user['dicPatientData']), flush=True)
        logged_in_user['dicCoverageData'] = dic_coverage_data['response'].json()
        print(json.dumps(logged_in_user['dicCoverageData']), flush=True)
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
    *
    * Insurance info of the bene is extracted from the C4DIC resources Patient,
    * Coverage (fetched from the BB2 server and cached in logged_in_user), and 
    * sent back to FE to render a CMS insurance 'card'
    """

    print_setting()

    ## C4DIC patient and coverage where to extract PII and coverage plans & eligibilities
    dic_patient = logged_in_user.get('dicPatientData')
    dic_coverage = logged_in_user.get('dicCoverageData')
    ## a empty insurance response
    coverages = []
    insurance = {'coverages': coverages}
    ## a response
    resp = {'insData': insurance}

    if logged_in_user and dic_patient and dic_coverage:
        ## extract info from C4DIC Patient and Coverage
        ## and composite into insurance info and response to
        ## FE for insurance card rendering
        ## Note, Coverage could be paged, not iterate page here for POC purpose

        ## From C4DIC Patient extract:
        ## 1. identifier mbi, e.g. 1S00EU7JH47
        ## 2. name, e.g. Johnie C
        ## From C4DIC Coverage extract:
        ## 1. coverage class: by Coverage resource 'class': "Part A"
        ## 2. status: active or not active
        ## 3. period, start date: e.g. 2014-02-06
        ## 4. payor: CMS
        ## 5. contract number: e.g. Part D , Part C: ptc_cntrct_id_01...12
        ## 6. reference year: e.g. Part A: 2025, Part B: 2025, etc.
        ## 7. other info such as: DIB, ESRD etc. can be added as needed
        pt = dic_patient['entry']
        patient = pt[0]
        mbi = lookup_1_and_get("$.resource.identifier[?(@.system=='http://hl7.org/fhir/sid/us-mbi')]", "value", patient)
        if len(mbi) == 11:
            mbi = mbi[0:4] + '-' + mbi[4:7] + '-' + mbi[7:]
        insurance['identifier'] = mbi
        # TODO: handle wider variety of given/family names
        pt_name = patient['resource']['name'][0]['given'][0] + " " + patient['resource']['name'][0]['family']
        insurance['name'] = pt_name

        coverage_array = dic_coverage['entry']

        for c in coverage_array:
            coverage = {}
            c_resource_id = c['resource'].get('id')
            c_coverageClass = lookup_1_and_get("$.resource.class[?(@.type.coding[0].code=='plan')]", "value", c)
            if c_coverageClass and (c_coverageClass != "Part A" or c_coverageClass != "Part B"):
                if "c4dic-part-c" in c_resource_id:
                    c_coverageClass = "Part C"
                elif "c4dic-part-d" in c_resource_id:
                    c_coverageClass = "Part D"
            coverage['coverageClass'] = c_coverageClass if c_coverageClass else "Null"
            c_status = c['resource']['status']
            coverage['status'] = c_status
            c_medicaidEligibility = "FULL"
            coverage['medicaidEligibility'] = c_medicaidEligibility
            c_period = c['resource'].get('period')
            c_start = c_period.get('start') if c_period else ""
            try: 
                c_start_date = datetime.strptime(c_start, '%Y-%m-%d').date()
                c_start = c_start_date.strftime("%b %d, %Y")
            except ValueError:
                pass # Some room for improvement here, but for now, we'll just use the original value from FHIR
            coverage['startDate'] = c_start if c_start else ""
            c_end = c_period.get('end') if c_period else ""
            coverage['endDate'] = c_end if c_end else ""
            c_payer = c['resource']['payor'][0]
            c_payer_org = "TO BE RESOLVED"
            c_contacts = []
            if c_payer:
                ## BFD C4DIC Coverage response: payer is a reference to the contained Organization
                ref_payer_org = c_payer['reference']
                if ref_payer_org:
                    ref_payer_org = ref_payer_org[1:] if ref_payer_org.startswith('#') else ref_payer_org
                    # can also extract more payer details, e.g. contact etc.
                    c_payer_org = lookup_1_and_get(f"$.resource.contained[?(@.id=='{ref_payer_org}')]", "name", c)
                    # contacts = lookup_by_path(f"$.resource.contained[?(@.id=='{ref_payer_org}')].contact[0].telecom", c)
                    contacts = lookup_1_and_get(f"$.resource.contained[?(@.id=='{ref_payer_org}')]", "contact", c)
                    if contacts[0]:
                        telecoms = contacts[0]['telecom']
                        for t in telecoms:
                            c_contacts.append(t['value'])

            coverage['payer'] = c_payer_org
            coverage['contacts'] = c_contacts
            c_contract_id = "" ## Part A and Part B does not have contract number
            if c_coverageClass == "Part C":
                c_contract_id = lookup_1_and_get("$.resource.class[?(@.type.coding[0].code=='plan')]", "value", c)
                # c_contract_id = lookup_1_and_get(f"$.resource.extension[?(@.url=='{CMS_VAR_PTC_CNTRCT_ID_01}')]", "valueCoding", c).get('code')
            if c_coverageClass == "Part D":
                c_contract_id = lookup_1_and_get("$.resource.class[?(@.type.coding[0].code=='plan')]", "value", c)
                # c_contract_id = lookup_1_and_get(f"$.resource.extension[?(@.url=='{CMS_VAR_PTD_CNTRCT_ID_01}')]", "valueCoding", c).get('code')
            coverage['contractId'] = c_contract_id
            c_reference_year = lookup_1_and_get(f"$.resource.extension[?(@.url=='{CMS_VAR_REF_YR}')]", "valueDate", c)
            coverage['referenceYear'] = c_reference_year
            # color palettes extension
            c_color_palette_ext = lookup_by_path(f"$.resource.extension[?(@.url=='{C4DIC_COLOR_PALETTE_EXT}')]", c)
            if c_color_palette_ext[0]:
                # another layer of extension for color codes per C4DIC profile
                palette_ext = c_color_palette_ext[0].value['extension']
                for p in palette_ext:
                    color_code_url = p['url']
                    if color_code_url == C4DIC_COLOR_BG:
                        c_color_palette_ext_bg = p['valueCoding']['code']
                    if color_code_url == C4DIC_COLOR_FG:
                        c_color_palette_ext_fg = p['valueCoding']['code']
                    if color_code_url == C4DIC_COLOR_HI_LT:
                        c_color_palette_ext_hi_lt = p['valueCoding']['code']
                # set color palette
                # fg #F4FEFF Light blue
                # bg #092E86 Navy
                # hi lt: #3B9BFB sky blue
                coverage['colorPalette'] = {
                    "foreground": c_color_palette_ext_fg,
                    "background": c_color_palette_ext_bg,
                    "highlight": c_color_palette_ext_hi_lt,
                }
            c_logo_ext = lookup_1_and_get(f"$.resource.extension[?(@.url=='{C4DIC_LOGO_EXT}')]", "valueString", c)
            coverage['logo'] = c_logo_ext
            c_addl_card_info_ext = lookup_1_and_get(f"$.resource.extension[?(@.url=='{C4DIC_ADDL_CARD_INFO_EXT}')]", "valueAnnotation", c).get('text')
            coverage['addlCardInfo'] = c_addl_card_info_ext

            coverages.append(coverage)

        insurance['coverages'] = coverages
    
    return resp


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
