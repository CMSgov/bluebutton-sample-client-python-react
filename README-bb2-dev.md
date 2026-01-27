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

### Testing Locally

This information is repeated from the SDK (https://github.com/CMSgov/cms-bb2-python-sdk/blob/main/README-sdk-dev.md). It is here for ease of reference as it contains steps relating to the sample client as well.
The current method for seeing the SDK in action is fairly complex, as it requires also setting up the Python sample client (this repo). These both, of course, depend upon the web-server repo for most of their logic. It is possible that in order to fully understand an issue that arises within the SDK or the sample client, a developer would have to track changes across 3 separate projects. There should be some future work to simplify this process as it is very manual and laborious.

The steps listed here are listed elsewhere in the documentation but for the sake of convenience, they are partially repeated here
and written together so that a developer should be able to follow this step by step.

The overall goals are to:

  - Build a local version of the SDK
  - Run a local version of sample client that consumes a local version of the SDK

  ### Building a local version of the SDK

    Run the following commands in the base of the SDK repository. The commands suppose that you have the Python sample client cloned in the same folder as this SDK repo. Do not be in a virtualenv while running these commands.

    ```
      rm -rf build/
      python -m build --wheel --o ../bluebutton-sample-client-python-react/server
    ```

    The --o (or outdir) command should effectively 'copy paste' the built version of the .whl file into where it would be needed for the sample client. If you do not want it in the sample client, omit the --o and file path.

  ### Run a local version of sample client that consumes a local version of the SDK

    Ensure that in bluebutton-sample-client-python-react/server/Dockerfile, uncomment the following line. Replace the version number (1.0.4 in the example) of the .whl file with what has been generated from the previous build command.

    ```
      RUN pip install cms_bluebutton_sdk-1.0.4-py3-none-any.whl
    ```
    
    In bluebutton-sample-client-python-react/server/Pipfile, add this line:

    ```
      cms-bluebutton-sdk = {file = "./cms_bluebutton_sdk-1.0.4-py3-none-any.whl"}
    ```

    In the base repository of bluebutton-sample-client-python-react, run the following commands. Ensure that you have no currently running containers or images of the sample client.

    ```
      cd server
      unzip -l cms_bluebutton_sdk-1.0.4-py3-none-any.whl
      pip install cms_bluebutton_sdk-1.0.4-py3-none-any.whl
      docker compose up
    ```

  Each time a change is made in the SDK, you must repeat all of the previous steps of building and re-running a local sample client. You must also ensure that the containers and images are removed each time.