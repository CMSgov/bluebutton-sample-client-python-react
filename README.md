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

```    
    cp server/sample-bluebutton-config.json server/.bluebutton-config.json
```

Make sure to replace the client_id and client_secret variables within the config file with
the ones you were provided, for your application, when you created your Blue Button Sandbox account,
the supported environments are SANDBOX or PRODUCTION.

```
    docker-compose up -d
```

This single command will create the docker container with all the necessary packages, configuration, and code to 
run both the front and back ends of this sample application.

To run the front-end (client component listening on port 3000) in preview mode, set environment variable BB2_APP_LAUNCH=preview when launch docker-compose:

```
   BB2_APP_LAUNCH=preview docker-compose up -d
```

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
debugpy remote debugging enabled on port 10678 for server in docker compose, developer can attach to server from IDE e.g. vscode.

To set up the run config to debug in vscode, add below contents to `.vscode/launch.json`
```
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "0.0.0.0",
        "port": 10678
      },
      "justMyCode": false,
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}/server",
          "remoteRoot": "/server"
        }
      ]
    }
  ]
}
```

Error Responses and handling:
-----------------------------
[See ErrorResponses.md](./ErrorResponses.md)