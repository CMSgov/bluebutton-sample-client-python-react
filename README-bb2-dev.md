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
You can also start your configuration by following the sample config template for selenium tests:

cp server/sample-bluebutton-selenium-config.json server/.bluebutton-config.json

You will also need to add this URL to your `redirect_uris` list in your application's configuration on the BB2 Sandbox UI.

Go to local repository base directory and run docker compose as below:

docker-compose -f docker-compose.selenium.yml up --abort-on-container-exit

Note: --abort-on-container-exit will abort client and server containers when selenium tests ends

Note: You may need to clean up already existing Docker containers, if you are having issues or have changed your configuration file.

## Use default data sets

Instead of using the BB2 API to retrieve data from a BB2 server every time you run the
sample client, you can alternatively pre-populate json content to be loaded. To do so,
replace the json files in `server/default_datasets/Dataset 1` with your desired default
data, and then in `client/src/components/patientData.tsx`, update the 
`useDefaultDataButton` const to `true`. 

Then on the landing page of the sample client, in addition to the normal button
`Authorize` which can be used to query a BB2 server, there will also be a
`Load default data` button which can be used to load the data from the json files.

This is useful when developing front-end content since it shortens the amount of time
it takes to load sample data.

## Visual trouble shoot

Install VNC viewer and point browser to http://localhost:5900 to monitor web UI interactions

## Installing cms-bluebutton-sdk from test.pypi.org

The package can be installed from the test instance of the PyPI site for development testing. The default behavior is to install from the main site.

To utilize the test.pypi.org repository use the following commands:

To create and start the containers:

```
BUILD_DEVELOPMENT="True" docker-compose up -d
```

To build just the `server` container:

```
BUILD_DEVELOPMENT="True" docker-compose up -d --build server
```
OR
```
docker-compose build server --build-arg BUILD_DEVELOPMENT="True"
```

To show the version installed:

```
docker-compose exec server pip show cms-bluebutton-sdk
```

