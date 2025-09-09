BlueButton Sample Python Client Application
=====================================================

## Project Description
A sample application, written in Python with Flask and the Python SDK

## About the Project
The [Blue Button 2.0 API](https://bluebutton.cms.gov/) provides Medicare enrollee claims data to applications using the [OAuth2.0 authorization flow](https://datatracker.ietf.org/doc/html/rfc6749). We aim to provide a developer-friendly, standards-based API that enables people with Medicare to connect their claims data to the applications, services, and research programs they trust.

## Core Team
A list of core team members responsible for the code and documentation in this repository can be found in [COMMUNITY.md](COMMUNITY.md).

## Development and Software Delivery Lifecycle
The following guide is for members of the project team who have access to the repository as well as code contributors. The main difference between internal and external contributions is that external contributors will need to fork the project and will not be able to merge their own pull requests. For more information on contributing, see: [CONTRIBUTING.md](./CONTRIBUTING.md).

# Local Development

## Repository Structure
```
├── client
│   ├── public
│   ├── src
├── server
├── selenium_tests
```

## Setup

### Create a Blue Button Sandbox Account 
Create an account at the link below, and register your test application, to get your Blue Button Sandbox Credentials which will allow you to 
access the Blue Button synthetic data.  These credentials will be necessary to run this sample application as well as 
utilize the Blue Button data within your own applcation.

https://sandbox.bluebutton.cms.gov/v1/accounts/create

To ensure this sample application will work properly, make sure that when you register your application you add 
the following url (see below) under the 'Callback URLS/Redirect Uris' section:

http://localhost:3001/api/bluebutton/callback/

When you are ready to run your own application, you can change this value to the url that you need.  
Just log into your Blue Button Sandbox account and select 'View/Edit App->'.

## Installation
Install and setup Docker.  Go to https://docs.docker.com/get-started/ and follow the directions.

Install Python: https://www.python.org/downloads/

## Running
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

## Developing
Read the comments in the code to understand the application and where
you will need to make adjustments/changes as well as some suggestions
for best practices.

### BB2 Sandbox User
To ensure data displays properly in the sample application please use a 
Blue Button Sandbox user that has PDE (Part-D Events) EoBs (Explanation of Benefits).  An example of a user with this
data would be:  BBUser10000 (PWD: PW10000!) or BBUser09999 (PWD: PW09999!)


### Python SDK
The sample app utilizes our [Python SDK](https://github.com/CMSgov/cms-bb2-python-sdk).

Please review our SDK documentation for more information and additional features available for your use.

## Debugging
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

### Error Responses and handling:
[See ErrorResponses.md](./ErrorResponses.md)

# Contributing
Thank you for considering contributing to an Open Source project of the US Government! For more information about our contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Branching Model
This project follows standard GitHub flow practices:

* Make changes in feature branches and merge to `main` frequently
* Pull-requests are reviewed before merging
* Tests should be written for changes introduced
* Each change should be deployable to production

<!-- # Community

# Community Guidelines -->

# Governance
For more information about our governance, see [GOVERNANCE.md](GOVERNANCE.md).

# Feedback
Got questions? Need help troubleshooting? Want to propose a new feature? Contact the Blue Button 2.0 team and connect with the community in our [Google Group](https://groups.google.com/forum/#!forum/Developer-group-for-cms-blue-button-api).

# Policites

# Public Domain
This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/) as indicated in [LICENSE](LICENSE).

All contributions to this project will be released under the CC0 dedication. By submitting a pull request or issue, you are agreeing to comply with this waiver of copyright interest.

---------------
    





