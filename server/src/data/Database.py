# Database.py

from ..entities.Settings import Settings

""" DEVELOPER NOTES:
* This is our mocked DB - we are using python global variables to simulate an actual DB
"""

basicAuthToken = {
        'access_token' : '',
        'expires_in' : 0,
        'expires_at' : 0,
        'token_type' : '',
        'scope' : '',
        'refresh_token' : '',
        'patient' : ''
}

basicUser = {
        'authToken' : basicAuthToken,
        'name' : '',
        'userName' : '',
        'pcp' : '',
        'primaryFacility' : '',
        'eobData' : ''
}

DBusers = [basicUser]
DBsettings = Settings('','','')
DBcodeChallenge = dict['codeChallenge' : '','verifier' : '']
DBcodeChallenges = {'' : DBcodeChallenge}
DBid = 1

"""
* DEVELOPER NOTES:  
* 
* We are hard coding a Mock 'User' here of our demo application to save time
* creating/demoing a user logging into the application.
* 
* This user will then need to linked to the Medicare.gov login
* to approve of having their medicare data accessed by the application
* these login's will be linked/related so anytime they login to the 
* application, the application will be able to pull their medicare data.
* 
* Just for ease of getting and displaying the data
* we are expecting this user to be linked to the 
* BB2 Sandbox User BBUser29999 or BBUser29998
"""
def initDB():
        
    sampleUser = basicUser
    sampleUser.update({'name':'John Doe'})
    sampleUser.update({'username':'jdoe29999'})
    sampleUser.update({'pcp':'Dr. Hibbert'})
    sampleUser.update({'primaryFacility':'Springfield General Hospital'})
    DBusers.append(sampleUser)
