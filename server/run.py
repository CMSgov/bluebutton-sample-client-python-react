# run.py
from src.shared.LoggerFactory import LoggerFactory
from src.prestart.setenv import setEnvVariables
from src.data.Database import *
from src.app import app
import os
import sys

"""
This is the starting point of the server side of the application.  This file is first ran to 
    create a socket where the server will listen for requests via the views.py
"""

# here we must initiliaze our global variables that are acting like a Mocked up Database 
# from Database.py (using the initDB() funciton)

initDB()
# set the path base for later use
main_base = os.path.dirname(__file__)
# initialize the logger object
myLogger = LoggerFactory.get_logger(log_file=__name__,log_level='DEBUG')

# here is where the rubber meets the road
if __name__ == "__main__":
    # set the necessary environment variables
    # as well as pull settings and config data from files based upon
    # the command line/environment variables set when executing the application
    os.environ['FLASK_APP'] = 'run.py'

    # Load the configs    
    if len(sys.argv)>2 and sys.argv[1] == "--ENV":
        dotenv_path = os.path.join(main_base,'src','prestart','env',sys.argv[2]+'.env')     
        print('DOTENV1: '+dotenv_path)  
        os.environ['FLASK_ENV'] = sys.argv[2]        
    elif len(sys.argv) <= 2:
        dotenv_path = os.path.join(main_base,'src','prestart','env','development.env')
        print('DOTENV2: '+dotenv_path)  
        os.environ['FLASK_ENV'] = 'development'
    try:
        setEnvVariables(dotenv_path=dotenv_path)    
        app.run(host=os.getenv('HOST'),port=os.getenv('PORT'))    
    except BaseException as err:
        """DEVELOPER NOTES:
        * This is where you could also use a data service or other exception handling
        * to display or store the error
        """
        myLogger.error(err)
   