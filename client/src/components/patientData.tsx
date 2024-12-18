import { Button } from '@cmsgov/design-system';
import axios from 'axios';
import chart from '../images/who-charted.png'
import { SettingsType } from '../types/settings';
import React, { useState } from 'react';

export default function PatientData() {
    const [header] = useState('Fetch your Coverage and Medicare Prescription Drug data');
    const [settingsState] = useState<SettingsType>({
        useDefaultDataButton: true,
    });
    async function goAuthorize() {
        const authUrlResponse = await axios.get(`/api/authorize/authurl`);
        window.location.href = authUrlResponse.data || '/';
    }    
    async function goLoadDefaults() {
        const loadDefaultsData = await axios.get(`/api/bluebutton/loadDefaults`);
        window.location.href = loadDefaultsData.data || '/';
    }  
    async function goLoadDefaults2() {
        const loadDefaultsData = await axios.get(`/api/bluebutton/loadDefaults2`);
        window.location.href = loadDefaultsData.data || '/';
    }  
    
    /* DEVELOPER NOTES:
    * Here we are hard coding the users information for the sake of saving time
    * you would display user information that you have stored in whatever persistence layer/mechanism 
    * your application is using
    */
    return (
        <div>
            <h3>Medicare Coverage and Prescription Drug Records</h3>
            <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start">
                <img src={chart} alt="Chart icon" className=""/>
                <p className='ds-u-padding-x--2 ds-u-margin-top--0'>
                    You can now allow Springfield General Hospital access to your Coverage and Medicare prescription drug records!
                </p>
            </div>
            <div className='ds-u-margin-top--2 ds-u-border-top--2'>
                <div>
                    <h4>{ header }</h4>
                </div>
                <div className='ds-u-margin-top--2'>
                    <Button id="auth_btn" variation="primary" onClick={goAuthorize}>Authorize</Button>
                </div>
                {
                    settingsState.useDefaultDataButton ?
                    <div>
                        <div className='ds-u-margin-top--2'>
                            <Button id="load_defaults_btn" variation="primary" onClick={goLoadDefaults}>Load default data 1</Button>
                        </div>
                        <div className='ds-u-margin-top--2'>
                            <Button id="load_defaults_btn2" variation="primary" onClick={goLoadDefaults2}>Load default data 2</Button>
                        </div>
                    </div> :
                        null
                }
            </div>
        </div>
    );
}