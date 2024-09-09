import React from 'react';
import Header from './components/header';
import Patient from './components/patient';
import PatientData from './components/patientData';
import InsuranceCard from './components/c4dic'
import Records from './components/records';
import { BrowserRouter as Router} from "react-router-dom";
import { TabPanel, Tabs } from '@cmsgov/design-system';

function App() {
  if (window.location.pathname.endsWith('card_only')) {
    return (
      <div className="ds-l-container ds-u-margin-bottom--7 ds-u-padding-bottom--7">
      <Router>
        <div className="bb-c-c4dic-card-png default-card">
            <InsuranceCard />
        </div>
      </Router>
      </div>
    );
  }
  else {
    return (
      <div className="ds-l-container ds-u-margin-bottom--7 ds-u-padding-bottom--7">
      <Router>
        <Header />
        <div>
          <p className='ds-u-measure--base'>
                Blue Button 2.0 is a standards-based application programming interface (API) that delivers Medicare Part A, B, and D data for over 60 million Medicare beneficiaries. <a href="https://bluebutton.cms.gov/">Learn more about Blue Button 2.0</a>
          </p>
  
          <p className='ds-u-measure--base'>
            The CMS design system is a set of open source design and front-end development resources for creating Section 508 compliant, responsive, and consistent websites. It builds on the U.S. Web Design System and extends it to support additional CSS and React components, utility classes, and a grid framework to allow teams to quickly prototype and build accessible, responsive, production-ready websites. <a href="https://design.cms.gov/">Learn more about CMS Design System</a>
          </p>
        </div>
  
        <Tabs tablistClassName="ds-u-margin-top--3">
          <TabPanel id="patient" tab="Patient">
            <div className="ds-u-display--flex ds-u-flex-direction--column ds-u-lg-flex-direction--row ds-u-flex-wrap--nowrap ds-u-lg-flex-wrap--wrap">
              <table>
                <tr>
                  <td>
              <div className="bb-c-card default-card">
                <Patient />
              </div>          
                  </td>
                  <td>
              <div className="bb-c-card default-card">
                <PatientData />
              </div>          
                  </td>
                </tr>
              </table>
            </div>
          </TabPanel>
          <TabPanel id="claims" tab="Claims">
            <div>
              <Records /> 
            </div>
          </TabPanel>
          <TabPanel id="dic-new-design" tab="Insurance Card">
            <a href='/card_only' target="_blank">Show in new window</a>
            <div className="bb-c-c4dic-card-png default-card">
                <InsuranceCard />
            </div>
          </TabPanel>
        </Tabs>
      </Router>
      </div>
    );  
  }
}

export default App;
