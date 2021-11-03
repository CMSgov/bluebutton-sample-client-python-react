# DEVELOPER NOTES:
# Copy this file and rename it to config.py
# Replace your client/secret/callback url for each environment below with your specific app details
# (Note: local is mainly for BB2 internal developers)

ConfigType = {
    'production' : {
        'bb2BaseUrl' : 'https://api.bluebutton.cms.gov',
        'bb2ClientId' : '<client-id>',
        'bb2ClientSecret' : '<client-secret>',
        'bb2CallbackUrl' : '<only https is supported in prod>',
        'port' : 3001,
        'host' : 'Unk'
    },
    'sandbox' : {
        'bb2BaseUrl' : 'https://sandbox.bluebutton.cms.gov',
        'bb2ClientId' : '<client-id>',
        'bb2ClientSecret' : '<client-secret>',
        'bb2CallbackUrl' : 'http://server:3001/api/bluebutton/callback/',
        'port' : 3001,
        'host' : 'server'
    },
    'local' : {
        'bb2BaseUrl' : 'https://sandbox.bluebutton.cms.gov',
        'bb2ClientId' : '<client-id>',
        'bb2ClientSecret' : '<client-secret>',
        'bb2CallbackUrl' : 'http://server:3001/api/bluebutton/callback/',
        'port' : 3001,
        'host' : 'server'
    }
}

