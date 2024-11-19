import { Table, TableCaption, TableRow, TableCell, TableHead, TableBody } from '@cmsgov/design-system';
import React, { useEffect, useState } from 'react';

// From C4DIC Patient extract:
// 1. identifier mbi, e.g. 1S00EU7JH47
// 2. name, e.g. Johnie C
// From C4DIC Coverage extract:
// 1. coverage class: by Coverage resource 'class': "Part A"
// 2. status: active or not active
// 3. period, start date: e.g. 2014-02-06
// 4. payor: CMS
// 5. contract number: e.g. Part D , Part C: ptc_cntrct_id_01...12
// 6. reference year: e.g. Part A: 2025, Part B: 2025, etc.
// 7. other info such as: DIB, ESRD etc. can be added as needed

export type CoverageInfo = {
    coverageClass: string,
    contractId: string,
    startDate: string,
    endDate: string,
    payer: string,
    status: string,
    medicaidEligibility: string,
    referenceYear: string,
    colorPalette: {
        foreground: string,
        background: string,
        highlight: string
    },
    logo: string,
    addlCardInfo: string,
    contacts: string[]
}

export type InsuranceInfo = {
    name: string,
    identifier: string, // mbi
    coverages: CoverageInfo[] // e.g. Part A, Part B, Part C, Part D
}

export type ErrorResponse = {
    type: string,
    content: string,
}

export default function InsuranceCard() {
    const [insInfo, setInsInfo] = useState<InsuranceInfo>();
    const [message, setMessage] = useState<ErrorResponse>();
    /*
    * DEVELOPER NOTES:
    */
    useEffect(() => {
        fetch('/api/data/insurance')
            .then(res => {
                return res.json();
            }).then(insuranceData => {
                if (insuranceData.insData) {
                    const coveragesList: CoverageInfo[] = insuranceData.insData?.coverages.map((c: any) => {
                        return {
                            coverageClass: c.coverageClass,
                            payer: c.payer,
                            contractId: c.contractId,
                            startDate: c.startDate,
                            endDate: c.endDate,
                            status: c.active,
                            medicaidEligibility: c.medicaidEligibility,
                            referenceYear: c.referenceYear,
                            colorPalette: {
                                foreground: c.colorPalette.foreground,
                                background: c.colorPalette.background,
                                highlight: c.colorPalette.highlight
                            },
                            logo: c.logo,
                            addlCardInfo: c.addlCardInfo,
                            contacts: c.contacts
                        }
                    });

                    setInsInfo(
                        {
                            name: insuranceData.insData.name,
                            identifier: insuranceData.insData.identifier,
                            coverages: coveragesList
                        }
                    );
                }
                else {
                    if (insuranceData.message) {
                        setMessage({"type": "error", "content": insuranceData.message || "Unknown"})
                    }
                }
            });
    }, [])

    if (message) {
        return (
            <div className='full-width-card'>
                <Table className="ds-u-margin-top--2" stackable stackableBreakpoint="md">
                    <TableCaption>Error Response</TableCaption>
                    <TableHead>
                        <TableRow>
                            <TableCell id="column_1">Type</TableCell>
                            <TableCell id="column_2">Content</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        <TableRow>
                            <TableCell stackedTitle="Type" headers="column_1">
                                {message.type}
                            </TableCell>
                            <TableCell stackedTitle="Content" headers="column_2">
                                {message.content}
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        );
    } else {
        var backgroundColor = insInfo?.coverages[0]?.colorPalette.background
        var highlightColor = insInfo?.coverages[0]?.colorPalette.highlight
        var textColor = insInfo?.coverages[0]?.colorPalette.foreground
        const root = document.documentElement;
        if (backgroundColor != null) {
            root.style.setProperty('--c4dic-backgroundColor', backgroundColor);
        }
        if (highlightColor != null) {
            root.style.setProperty('--c4dic-highlightColor', highlightColor);
        }
        if (textColor != null) {
            root.style.setProperty('--c4dic-textColor', textColor);
        }
        const medicaidEligibility = (insInfo?.coverages[0]?.medicaidEligibility != null) ? 
        (
            <div>
                <text className="field-label">Medicaid Eligibility</text>
                <br/>
                <div className="bb-c-c4dic-badge-container">
                    <div className="bb-c-c4dic-badge">{insInfo?.coverages[0]?.medicaidEligibility}</div>
                </div>
            </div>
        ) : null
        return (
            <div className="ins-c4dic-card">
                <div className="bb-c-c4dic-card-header">
                    <img src={insInfo?.coverages[0]?.logo} alt="C4DIC Logo" height="48px"/>
                    <h3>{insInfo?.coverages[0]?.payer}</h3>
                </div>
                <div className="pii-sec bb-c-c4dic-card-pii-area">
                    <div className="ins-fld-text patient-name">
                        <div>
                            <text className="field-label">Name</text>
                            <br/>
                            <text className="field-value">{insInfo?.name||""}</text>
                        </div>
                    </div>
                    <div className="ins-fld-text patient-info">
                        <div>
                            <text className="field-label">Medicare Number</text>
                            <br/>
                            <text className="field-value">{insInfo?.identifier||""}</text>
                        </div>
                        {medicaidEligibility}
                    </div>
                </div>

                <div className="coverage-sec bb-c-c4dic-card-coverages-area">
                    <hr/>
                    <h6>Benefits</h6>
                    {insInfo?.coverages.map(c => {
                            const startDateDiv = (c.startDate !== null && c.startDate !== "") ?
                                (
                                    <div> 
                                        <text className="field-label">Start Date</text>
                                        <br/>
                                        <text className="field-value">{c.startDate}</text>
                                    </div>
                                ) : null
                            switch (c.coverageClass) {
                                case "Part A":
                                    return (
                                        <div className="bb-c-c4dic-coverage-a">
                                            <div> 
                                                <text className="field-label">Coverage</text>
                                                <br/>
                                                <text className="field-value">Hospital<br/>{c.coverageClass}</text>
                                            </div>
                                            {startDateDiv}
                                            <div> 
                                                <text className="field-label">Entitlement Reason</text>
                                                <br/>
                                                <text className="field-value">{c.contractId}</text>
                                            </div>
                                        </div>
                                    )
                                case "Part B":
                                    return (
                                        <div className="bb-c-c4dic-coverage-b">
                                            <div> 
                                                <text className="field-label">Coverage</text>
                                                <br/>
                                                <text className="field-value">Medical<br/>{c.coverageClass}</text>
                                            </div>
                                            {startDateDiv}
                                        </div>
                                    )
                                case "Part C":
                                    const partCTypeDiv = (c.coverageClass != null) ? 
                                    (
                                        <div> 
                                            <text className="field-label">Type</text>
                                            <br/>
                                            <text className="field-value">{c.coverageClass}</text>
                                        </div>
                                    ) : null
                                    return (
                                        <div className="bb-c-c4dic-coverage-c">
                                            <div> 
                                                <text className="field-label">Coverage</text>
                                                <br/>
                                                <text className="field-value">Advantage<br/>{c.coverageClass}</text>
                                                {partCTypeDiv}
                                            </div>
                                            <div> 
                                                <text className="field-label">Plan #</text>
                                                <br/>
                                                <text className="field-value">{c.contractId}</text>
                                                <br/>
                                                <text className="field-label">Organization</text>
                                                <br/>
                                                <text className="field-value">{c.payer}</text>
                                            </div>
                                        </div>
                                    )
                                case "Part D":
                                    return (
                                        <div className="bb-c-c4dic-coverage-d">
                                            <div> 
                                                <text className="field-label">Coverage</text>
                                                <br/>
                                                <text className="field-value">Rx<br/>{c.coverageClass}</text>
                                            </div>
                                            {startDateDiv}
                                            <div>
                                                <text className="field-label">Plan #</text>
                                                <br/>
                                                <text className="field-value">{c.contractId}</text>
                                            </div>
                                        </div>
                                    )
                                default:
                                    return []
                            }
                        })}
                </div>
                <div className="bb-c-c4dic-card-org-contact">
                    <hr/>
                    <h6>Contact</h6>

                    <text className="field-label">Customer Service</text>
                    <br/>
                    <div className="contact-list">
                    {insInfo?.coverages[0]?.contacts.map(contact => {
                        return <text className="field-value">{contact}</text>
                    })}
                    </div>
                    <br/>
                </div>
                <div className="bb-c-c4dic-card-additional-card-info">
                    <text>{insInfo?.coverages[0]?.addlCardInfo}</text>
                </div>
            </div>
        );
    }
}
