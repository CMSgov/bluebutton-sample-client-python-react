from ..data.Database import *

"""
DEVELOPER NOTES:
* Here we are literally just grabbing the first user 
* in a mock list of users for the sample app
* This is where your app would have already authenticated the user
* and provided the details/data about that user to 
* the other services/portions of the application
"""

def get_loggedin_user():
    return DBusers[0]

def clear_bb2_data():
    logged_in_user = get_loggedin_user()
    logged_in_user.update({'authToken': {
        'access_token' : '',
        'expires_in' : 0,
        'expires_at' : 0,
        'token_type' : '',
        'scope' : '',
        'refresh_token' : '',
        'patient' : ''
    }})
    logged_in_user.update({'eobData': {}})
