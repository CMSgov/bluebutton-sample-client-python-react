""" 
* DEVELOPER NOTE:
* to utilize the latest security features/best practices
* it is recommended to utilize pkce
* 
* Default values are hard coded here, but you may choose to store these values in a
* config file or other mechanism
* 
* It's recommended that you use the latest version V2, which utilizes
* FHIR R4 
"""

class Settings(object):
    # set the initial values to their defaults here
    # but allow them to change via the constructor
    def __init__(self,env,version,pkce):
        self.env = env or 'sandbox'
        self.version = version or 'v2'
        if pkce is None or (pkce != True and pkce != False):
            self.pkce = True
        else:
            self.pkce = pkce
            