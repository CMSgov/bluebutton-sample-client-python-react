from ..data.Database import *

"""
DEVELOPER NOTES:
* Here we are literally just grabbing the first user 
* in a mock list of users for the sample app
* This is where your app would have already authenticated the user
* and provided the details/data about that user to 
* the other services/portions of the application
"""

def getLoggedInUser():
    return DBusers[0]
