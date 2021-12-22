Create a Blue Button Sandbox Account 
---------------
Create an account at the link below, and register your test application, to get your Blue Button Sandbox Credentials which will allow you to 
access the Blue Button synthetic data.  These credentials will be necessary to run this sample application as well as 
utilize the Blue Button data within your own applcation.  See the section below 'Running the Back-end & Front-end'.

https://sandbox.bluebutton.cms.gov/v1/accounts/create

To ensure this sample application will work properly, make sure that when you register your application you add 
the following url (see below) under the 'Callback URLS/Redirect Uris' section:

http://localhost:3001/api/bluebutton/callback/

When you are ready to run your own application, you can change this value to the url that you need.  
Just log into your Blue Button Sandbox account and select 'View/Edit App->'.

Setup Docker & Python 
---------------
Install and setup Docker.  Go to https://docs.docker.com/get-started/ and follow the directions.

Install Python: https://www.python.org/downloads/

Running the Back-end & Front-end
---------------
    
Once Docker and Python are Installed then do the following:
    
    copy server/src/configs/sample_config.py -> server/src/configs/config.py
    
Make sure to replace the clientId and clientSecret variables within the config file with
the ones you were provided, for your application, when you created your Blue Button Sandbox account.

    copy server/src/prestart/env/sandbox.sample.env -> server/src/prestart/env/development.env

    docker-compose up -d

This single command will create the docker container with all the necessary packages, configuration, and code to 
run both the front and back ends of this sample application.

To see the application in action open your browser and enter the following URL:

http://localhost:3000

To see the process of authenticating with Blue Button via Medicare.gov and retrieve EoB data just click on the 'Authorize' button.

BB2 Sandbox User
-----------
To ensure data displays properly in the sample application please use a 
Blue Button Sandbox user that has PDE (Part-D Events) EoBs (Explanation of Benefits).  An example of a user with this
data would be:  BBUser29999 (PWD: PW29999!) or BBUser29998 (PWD: PW29998!)

Development
-----------
Read the DEVELOPER NOTES found in the code to understand the application
and where you will need to make adjustments/changes as well as some 
suggestions for best practices.

Debugging server component
--------------------------
debugpy remote debugging enabled on port 5678 for server in docker compose, developer can attach to server from IDE e.g. vscode.
 