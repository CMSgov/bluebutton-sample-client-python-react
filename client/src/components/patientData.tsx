import { Button } from '@cmsgov/design-system';
import axios from 'axios';
import chart from '../images/who-charted.png'
import { SettingsType } from '../types/settings';
import React, { useState } from 'react';
import * as process from 'process'; 

export default function PatientData() {
    const [header] = useState('Add your Medicare Prescription Drug data');
    const [settingsState] = useState<SettingsType>({
        useDefaultDataButton: false, // Set to true to use hard coded data
    });
    async function goAuthorize() {
        const test_url = process.env.TEST_APP_API_URL ? process.env.TEST_APP_API_URL : ''
        const authUrlResponseData = await axios.get(`${test_url}/api/authorize/authurl`)
        .then(response => {
            return response.data;
        })
        .then(data => {
            window.location.href = data;
        })
        .catch(error => {
            window.location.href = "/";
        });
        console.log(authUrlResponseData);
    }    
    async function goLoadDefaults() {
        const loadDefaultsData = await axios.get(`/api/bluebutton/loadDefaults`);
        window.location.href = loadDefaultsData.data || '/';
    }    
    
    /* DEVELOPER NOTES:
    * Here we are hard coding the users information for the sake of saving time
    * you would display user information that you have stored in whatever persistence layer/mechanism 
    * your application is using
    */
    return (
        <div>
            <h3>Medicare Prescription Drug Records</h3>
            <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start">
                <img src={chart} alt="Chart icon" className=""/>
                <p className='ds-u-padding-x--2 ds-u-margin-top--0'>
                    John, you can now allow Springfield General Hospital access to your Medicare prescription drug records!
                </p>
            </div>
            <div className='ds-u-margin-top--2 ds-u-border-top--2'>
                <div>
                    <h4>{ header }</h4>
                </div>
                <div className='ds-u-margin-top--2'>
                    <Button id="auth_btn" variation="solid" onClick={goAuthorize}>Authorize</Button>
                </div>
                {
                    settingsState.useDefaultDataButton ?
                    <div className='ds-u-margin-top--2'>
                        <Button id="load_defaults_btn" variation="primary" onClick={goLoadDefaults}>Load default data</Button>
                    </div> :
                        null
                }
            </div>
        </div>
    );
}