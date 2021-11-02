# setenv.py
"""
 * Pre-start is where we want to place things that must run BEFORE the python script is executed.
 * This is useful for environment variables, command-line arguments, and cron-jobs.
"""
import os
from dotenv import load_dotenv

# set environment variables based upon the ENV file and the command line ENV
def setEnvVariables(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')
    os.environ['HOST'] = HOST
    os.environ['PORT'] = PORT
    os.environ['FLASK_APP'] = 'app.py'