Running backend & frontend
---------------
    
    copy server/src/configs/sample_config.py -> server/src/configs/config.py
    replace the secret variables with the ones for your application

    copy server/src/prestart/env/sandbox.sample.env -> server/src/prestart/env/development.env

    docker-compose up -d
    
BB2 Sandbox User
-----------
To ensure data displays properly in the sample application please use a 
Blue Button 2 Sandbox user that has PDE EoBs.  An example of a user with this
data would be:  BBUser29999 (PWD: PW29999!) or BBUser29998 (PWD: PW29998!)

Development
-----------
Read the DEVELOPER NOTES found in the code to understand the application
and where you will need to make adjustments/changes as well as some 
suggestions for best practices.

