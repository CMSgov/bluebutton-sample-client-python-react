import React from 'react'

export class DICClassic extends React.Component {

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
            insNum: "FAKE MBI",
            startDate: "FAKE DATE",
            fullName: "J SMITH Jr."
        };
        const settingsState = {
            pkce: true,
            version: 'v2',
            env: 'test'
        };
        // just reference the const to suppress compile time warning 
        if (settingsState === null)
            console.log("settingState is null...")
    }

    render() {
        return (
            <div className="content-wrapper">
                <div className="ins-classic-card">
                    <div className="ins-classic-card__front">

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
