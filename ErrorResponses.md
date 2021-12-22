# Blue Button 2.0 API Error Responses

## Overview

This document serves as a supplementary to Blue Button 2.0 API Developer Documents. It gives more details on the most common error responses and how to properly handle them.


## Error Responses and Client Actions

### Authorization Requests


| Status Code    | End Point URL   | Error Message              | Action            | Comments                                               |
| -------------- | --------------- | -------------------------- | ----------------- | ------------------------------------------------------ |
| 400<br>BAD REQUEST | /v[12]/o/.* | the response comes from blue button.<br>Example message:<br>error: unsupported grant type | Fix the request<br> | request has invalid parameter(s) |
| 403<br>FORBIDDEN | /v[12]/o/authorize/<br>/v[12]/o/authorize/(?P<uuid>[\w-]+)/$<br>/v[12]/o/token | You do not have permission to perform this action. |  | request does not pass permission check |
| 403<br>FORBIDDEN | /v[12]/o/authorize/<br>/v[12]/o/authorize/(?P<uuid>[\w-]+)/$ | This application, {your app name}, is temporarily inactive. <br>If you are the app maintainer, please contact the Blue Button 2.0 API team. <br>If you are a Medicare Beneficiary and need assistance, please contact the application's support team <br>or call 1-800-MEDICARE (1-800-633-4227) |  | the app is disabled by Blue Button 2.0 API administrator usually <br>due to abnormal usage pattern etc., contact CMS as instructed, <br>it is recommended to stop the app and resolve with Blue Button 2.0 API team |
| 404<br>NOT FOUND | /v[12]/o/.* | Medicare is unable to retrieve your data at this time due to an internal issue.<br>Our team is aware of the issue and is working to resolve it.<br>Please try again at a later time. We apologize for any inconvenience. |  | If any abnormality encountered during authorization, e.g. <br>the patient is not found by mbi hash / hicn hash lookup, the message will be <br>rendered as html page to the beneficiary, and with a 404 status code.<br>the authorization process aborted. |
| 502<br>BAD GATEWAY | /v[12]/o/.* | An error occurred connecting to medicare.gov account<br><br>other additional messages:<br><br>BBMyMedicareSLSxTokenException, or<br>BBMyMedicareSLSxSignoutException, or<br>BBMyMedicareSLSxValidateSignoutException, or<br>BBMyMedicareCallbackAuthenticateSlsUserInfoValidateException, or<br>BBMyMedicareSLSxUserinfoException at /mymedicare/sls-callback |  | Abnormality encountered during authorization for various causes as indicated by <br>error name in addition to the general message:<br><br>An error occurred connecting to medicare.gov account |
| 500<br>SERVER ERROR | /v[12]/o/.* | The root cause of the 500 error, some times, is indicated by the error message, <br>the app can choose to retry the failed request depend on the nature of the root cause, <br>examples that might be retriable are those related to network down (temporarily):<br>Example:<br>ConnectionError at /mymedicare/login<br>HTTPSConnectionPool(host='test.accounts.cms.gov', port=443): <br>Max retries exceeded with url: /health (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f46599dafd0>: <br>Failed to establish a new connection: [Errno -2] Name or service not known')) | | App retry on request during authorization<br>is not recommended. |


### Data Requests


| Status Code    | End Point URL   | Error Message              | Action            | Comments                                               |
| -------------- | --------------- | -------------------------- | ----------------- | ------------------------------------------------------ |
| 400<br>BAD REQUEST | /v[12]/fhir/.* | the response comes from FHIR data backend.<br>Example message:<br>details: IllegalArgumentException: Unsupported ID pattern | <br>Fix the request<br> | fhir request has invalid parameter(s) |
| 403<br>FORBIDDEN | /v[12]/fhir/.* | You do not have permission to perform this action. |  | the request is not in the scope of the grant authorized, <br>e.g. the beneficiary did not grant access to the demographic data |
| 403<br>FORBIDDEN | /v[12]/fhir/.* | This application, {your app name}, is temporarily inactive. <br>If you are the app maintainer, please contact the Blue Button 2.0 API team. <br>If you are a Medicare Beneficiary and need assistance, please contact the application's support team <br>or call 1-800-MEDICARE (1-800-633-4227) |  | the app is disabled by Blue Button 2.0 API administrator usually <br>due to abnormal usage pattern etc., contact CMS as instructed, <br>it is recommended to stop the app and resolve with Blue Button 2.0 API team |
| 404<br>NOT FOUND | /v[12]/fhir/.* | The requested resource does not exist |  | for example, for a fhir read request as:<br>/v2/fhir/Patient/-1234567890<br>but there is not a patient with<br>fhir_id = -1234567890, a 404 is returned |
| 502<br>BAD GATEWAY | /v[12]/fhir/.* | An error occurred contacting the upstream server: <error details><br>Example:<br>UpstreamServerException('An error occurred contacting the upstream server:Failed to call access method: <br>java.lang.IllegalArgumentException: _lastUpdate lower bound has an invalid prefix') |  | An error occurred in FHIR data backend when retrieving the resources, <br>it could be client side error e.g. a malformed query parameter in the URL where the error code should be 400 BAD REQUEST, <br>or a back end internal error.<br>the action on the 502 error is on a case by case basis, e.g. if the root cause of the 502 is actually a bad query parameter, <br>then retry is a sensible action. |
| 500<br>SERVER ERROR | /v[12]/fhir/.* | The root cause of the 500 error, some times, is indicated by the error message, <br>the app can choose to retry the failed request depend on the nature of the root cause, <br>examples that might be retriable are those related to network down (temporarily):<br>Example:<br>ConnectionError at /mymedicare/login<br>HTTPSConnectionPool(host='test.accounts.cms.gov', port=443): <br>Max retries exceeded with url: /health (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x7f46599dafd0>: <br>Failed to establish a new connection: [Errno -2] Name or service not known')) | Heuristic on Retry | App can choose to retry on some of the 500 errors as shown by the example, this is a heuristic approach. |


### Retry




Auto retrying (with sensible retry settings) on FHIR Data read/search to overcome a FHIR backend network temporary downtime is recommended.


Due to the involvement of the end user (beneficiary), auto retrying requests in the authorization flow are not recommended.

