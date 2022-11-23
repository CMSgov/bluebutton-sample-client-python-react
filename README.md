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
    
    cp server/sample-bluebutton-config.json server/.bluebutton-config.json

or (if running docker compose selenium tests)

    cp server/sample-bluebutton-selenium-config.json server/.bluebutton-config.json

Make sure to replace the client_id and client_secret variables within the config file with
the ones you were provided, for your application, when you created your Blue Button Sandbox account,
the supported environments are SANDBOX or PRODUCTION.

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
Read the comments in the code to understand the application and where
you will need to make adjustments/changes as well as some suggestions
for best practices.

Python SDK
----------

The sample app utilizes our [Python SDK](https://github.com/CMSgov/cms-bb2-python-sdk).

Please review our SDK documentation for more information and additional features available for your use.


Debugging server component
--------------------------
debugpy remote debugging enabled on port 5678 for server in docker compose, developer can attach to server from IDE e.g. vscode.

## Run selenium tests in docker

Configure the remote target BB2 instance where the tested app is registered (as described above "Running the Back-end & Front-end")

Also use below call back URL in configuration, and add it as redirect URI at Blue Button API app registry:

http://server:3001/api/bluebutton/callback/

Go to local repository base directory and run docker compose as below:

docker-compose -f docker-compose.selenium.yml up --abort-on-container-exit

Note: --abort-on-container-exit will abort client and server containers when selenium tests ends

## Visual trouble shoot

Install VNC viewer and point browser to http://localhost:5900 to monitor web UI interactions

Error Responses and handling:
-----------------------------
[See ErrorResponses.md](./ErrorResponses.md)