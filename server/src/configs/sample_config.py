# DEVELOPER NOTES:
# Copy this file and rename it to config.py
# Replace your client/secret/callback url for each environment below with your specific app details
# (Note: local is mainly for BB2 internal developers)



ConfigType = {
    'production': {
        'bb2BaseUrl': 'https://api.bluebutton.cms.gov',
        'bb2ClientId': '<client-id>',
        'bb2ClientSecret': '<client-secret>',
        'bb2CallbackUrl': '<only https is supported in prod>',
        'port': 3001,
        'host': 'Unk'
    },
    'sandbox': {
        'bb2BaseUrl': 'https://sandbox.bluebutton.cms.gov',
        'bb2ClientId': 't5NjtlGClce2fVXFor8yRVFa02zB5k9iVRTyoxV3',
        'bb2ClientSecret': 'lwfufptONF0rslSGZsxbisCl6bgNZB4QPU4OXr9FUoVut7dasuyiTf1Cx9oUZwoWctzMCzIGrkzkQaWRIhv9DmnNZludypUPrpyVr3kBhepUXjvdCgr5BBwAOILGnX2F',
        'bb2CallbackUrl': 'http://server:3001/api/bluebutton/callback/',
        'port': 3001,
        'host': 'server',
        'retry_settings': {
             "total": 3,
             "backoff_factor": 5,
             "status_forcelist": [500, 502, 503, 504]
         }
    },
    'local': {
        'bb2BaseUrl': 'https://sandbox.bluebutton.cms.gov',
        'bb2ClientId': '<client-id>',
        'bb2ClientSecret': '<client-secret>',
        'bb2CallbackUrl': 'http://localhost:3001/api/bluebutton/callback/',
        'port': 3001,
        'host': 'server'
    }
}

