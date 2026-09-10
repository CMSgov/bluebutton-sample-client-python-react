import React, { useEffect, useState } from 'react';
import * as process from 'process';

export type InsuranceCardInfo = {
    beneficiaryName: string,
    payerName: string,
    memberId: string,
    groupNumber: string,
    planNumber: string,
    effectiveDate: string
}

export type ErrorResponse = {
    type: string,
    content: string,
}

/*
* DEVELOPER NOTES:
* The digital insurance card is returned from the BB2 `$generate-insurance-card`
* operation (v3-only) as a CARIN Digital Insurance Card (C4DIC) FHIR Bundle
* containing Patient, Coverage, and Organization (payer) resources.
* See https://hl7.org/fhir/us/insurance-card/ for the full resource shapes.
*/
export default function InsuranceCard() {
    const [card, setCard] = useState<InsuranceCardInfo>();
    const [message, setMessage] = useState<ErrorResponse>();

    useEffect(() => {
        const test_url = process.env.TEST_APP_API_URL ? process.env.TEST_APP_API_URL : '';
        fetch(`${test_url}/api/data/insuranceCard`)
            .then(res => res.json())
            .then(bundleData => {
                console.log('Insurance card response:', JSON.stringify(bundleData, null, 2));
                if (bundleData.entry) {
                    const resources = bundleData.entry.map((entry: any) => entry.resource);
                    const patient = resources.find((r: any) => r?.resourceType === 'Patient');
                    const coverage = resources.find((r: any) => r?.resourceType === 'Coverage');
                    const organizations = resources.filter((r: any) => r?.resourceType === 'Organization');
                    const payerReference = coverage?.payor?.[0]?.reference?.split('/').pop();
                    const payer = organizations.find((r: any) => r?.id === payerReference) || organizations[0];

                    setCard({
                        beneficiaryName: patient?.name?.[0]?.text
                            || [patient?.name?.[0]?.given?.join(' '), patient?.name?.[0]?.family].filter(Boolean).join(' ')
                            || 'Unknown',
                        payerName: payer?.name || 'Unknown',
                        memberId: coverage?.subscriberId || coverage?.identifier?.[0]?.value || 'Unknown',
                        groupNumber: coverage?.class?.find((c: any) => c.type?.coding?.[0]?.code === 'group')?.value || 'Unknown',
                        planNumber: coverage?.class?.find((c: any) => c.type?.coding?.[0]?.code === 'plan')?.value || 'Unknown',
                        effectiveDate: coverage?.period?.start || 'Unknown',
                    });
                } else if (bundleData.message) {
                    setMessage({ type: 'error', content: bundleData.message });
                }
            });
    }, []);

    if (message) {
        return (
            <div className='full-width-card'>
                <p>{message.content}</p>
            </div>
        );
    }

    if (!card) {
        return null;
    }

    return (
        <div className="bb-c-card default-card">
            <h3>Digital Insurance Card</h3>
            <ul>
                <li>Beneficiary: {card.beneficiaryName}</li>
                <li>Payer: {card.payerName}</li>
                <li>Member ID: {card.memberId}</li>
                <li>Group Number: {card.groupNumber}</li>
                <li>Plan Number: {card.planNumber}</li>
                <li>Effective Date: {card.effectiveDate}</li>
            </ul>
        </div>
    );
}
