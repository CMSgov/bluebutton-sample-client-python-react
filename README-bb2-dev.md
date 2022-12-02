# Blue Button 2.0 Sample Application Development Documentation

## Introduction

This README contains information related to developing the SDK.

It is intended for BB2 team members or others performing sample application development work.

## Run selenium tests in docker

Configure the remote target BB2 instance where the tested app is registered (as described above "Running the Back-end & Front-end")

Change your `callback_url` configuration to use `server` instead of `localhost`. For example:
```JSON
    "callback_url": "http://server:3001/api/bluebutton/callback/"
```
can also start your configuration by the sample config template for selenium tests:

cp server/sample-bluebutton-selenium-config.json server/.bluebutton-config.json

You will also need to add this URL to your `redirect_uris` list in your application's configuration on the BB2 Sandbox UI.

Go to local repository base directory and run docker compose as below:

docker-compose -f docker-compose.selenium.yml up --abort-on-container-exit

Note: --abort-on-container-exit will abort client and server containers when selenium tests ends

Note: You may need to clean up already existing Docker containers, if you are having issues or have changed your configuration file.

## Visual trouble shoot

Install VNC viewer and point browser to http://localhost:5900 to monitor web UI interactions