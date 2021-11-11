import base64
import hashlib
import random
import string

"""
Here is where we handle everything PKCE - we need to mirror the options utilized by the Blue Button API 
So that verification can occur
"""
CodeChallenge = dict['codeChallenge' : '','verifier' : '']

def base64URLEncode(buffer) -> str:
    bufferBytes = base64.urlsafe_b64encode(buffer.encode("utf-8"))
    bufferResult = str(bufferBytes, "utf-8")
    return bufferResult

def getRandomString(length):
    # choose from all letters, digits and symbols
    letters = string.ascii_letters + string.digits + string.punctuation
    result = ''.join(random.choice(letters) for i in range(length))
    return result

def generateCodeChallenge():
    verifier = generateRandomState(32)
    myCodeChallenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode('ASCII')).digest())
    result: CodeChallenge = {'codeChallenge' : myCodeChallenge.decode('utf-8'), 'verifier' : verifier}
    return result

def generateRandomState(num):
    return base64URLEncode(getRandomString(num))
