import axios from 'axios';
import React from 'react'

export class DIC extends React.Component {

    /* DEVELOPER NOTES:
    * This is a minimal implementation with some sample calls to hardcoded
    * resources. Authorization isn't fully implemented because it follows a pattern
    * contrary to existing server usage (the call to an external service).
    *
    * Once hardcoded resources are deployed, this can be used as a toy to test DIC
    * implementation and design by adding a valid Bearer token to the Authorization header.
    *
    * In the long run, the profile querystring will be deprecated as well.
    */

    state: any;

    constructor(props: any) {
        super(props);
        this.state = {
            insNum: "",
            startDate: "",
            fullName: ""
        };
        const settingsState = {
            pkce: true,
            version: 'v2',
            env: 'test'
        };

        const DICResponse = axios.get(
            'https://test.bluebutton.cms.gov/v2/fhir/Patient?_profile=http://hl7.org/fhir/us/insurance-card/StructureDefinition/C4DIC-Patient',
            {
                params: settingsState,
                headers: {
                    Authorization: ""
                }
            },
        ).then((response: any) => {
            const fName = response['name'][0]['family'];
            const mName = response['name'][0]['given'][1];
            const lName = response['name'][0]['given'][0];
            this.state.insNum = response['identifier'][1]['value'];
            this.state.startDate = response['identifier'][1]['period']['start'];
            this.state.fullName = fName + mName + lName;
        }).catch((err: any) => console.log("Axios err: ", err));
    }

    render() {
        return (
            <div className="content-wrapper">
                <div className="ins-card">
                    <div className="ins-card__front">

                        <input value={this.state.insNum} className="card-number" placeholder="1234-234-1243-12345678901"/>

                        <div className="card-date-group">
                            <label htmlFor="card-date">Coverage Start Date</label>
                            <input value={this.state.startDate} className="card-date" placeholder="04/22"/>
                        </div>

                        <div className="card-name-group">
                            <label htmlFor="card-name">Member Name</label>
                            <input value={this.state.fullName} className="card-name" placeholder="John Smith"/>
                        </div>

                    </div>
                </div>
            </div>

        );
    }
}