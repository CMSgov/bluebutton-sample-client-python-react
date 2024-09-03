import { Table, TableCaption, TableRow, TableCell, TableHead, TableBody } from '@cmsgov/design-system';
import React, { useEffect, useState } from 'react';

// From C4DIC Patient extract:
// 1. identifier mbi, e.g. 1S00EU7JH47
// 2. name, e.g. Johnie C
// 3. gender, e.g. male
// 4. dob, e.g. 1990-08-14
// From C4DIC Coverage extract:
// 1. coverage class: by Coverage resource 'class': "Part A"
// 2. status: active or not active
// 3. period, start date: e.g. 2014-02-06
// 4. relationship to insured: e.g. self
// 5. payor: CMS
// 6. contract number: e.g. Part D , Part C: ptc_cntrct_id_01...12
// 7. reference year: e.g. Part A: 2025, Part B: 2025, etc.
// 8. other info such as: DIB, ESRD etc. can be added as needed

export type CoverageInfo = {
    clazz: string,
    contractId: string,
    startDate: string,
    endDate: string,
    payer: string,
    status: string,
    relationship: string, // self, spouse etc.
    referenceYear: string,
    cardImage: {
        description: string,
        label: string,
        image: {
            type: string,
            data: string
        }
    },
    c4dicSupportingImageSrc: string
}

export type InsuranceInfo = {
    name: string,
    gender: string,
    dob: string,
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
                            clazz: c.clazz,
                            payer: c.payer,
                            contractId: c.contractId,
                            startDate: c.startDate,
                            endDate: c.endDate,
                            status: c.active,
                            relationship: c.relationship,
                            referenceYear: c.referenceYear,
                            cardImage: {
                                description: c.cardImage.description,
                                label: c.cardImage.label,
                                image: {
                                    type: c.cardImage.image.type,
                                    data: c.cardImage.image.data
                                }
                            },
                            c4dicSupportingImageSrc: `data:image/png;base64,${c.cardImage.image.data}`
                        }
                    });

                    setInsInfo(
                        {
                            name: insuranceData.insData.name,
                            gender: insuranceData.insData.gender,
                            dob: insuranceData.insData.dob,
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
        return (
            <div className="content-wrapper">
                <div className="ins-c4dic-card">
                    <div className="pii-sec bb-c-c4dic-card-pii-area">
                        <pre className="ins-fld-text">Full Name: {insInfo?.name||""}    Gender: {insInfo?.gender||""}   DOB:  {insInfo?.dob||""}</pre>
                        <pre className="ins-fld-text">MBI: {insInfo?.identifier||""}</pre>
                    </div>

                    <div className="coverage-sec bb-c-c4dic-card-coverages-area">
                        {insInfo?.coverages.map(c => {
                                return (
                                    <div>
                                        <pre className="ins-fld-text">
                                            Coverage Type: {c.clazz}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Payer: {c.payer}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Contract Number: {c.contractId}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Start Date: {c.startDate}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            End Date: {c.endDate}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Status: {c.status}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Relationship to insured: {c.relationship||""}
                                        </pre>
                                        <pre className="ins-fld-text">
                                            Reference Year: {c.referenceYear}
                                        </pre>
                                        <img className="bb-c-card-img" src={c.c4dicSupportingImageSrc} alt="cardImage"></img>
                                    </div>
                                )
                            })}
                    </div>
                </div>
            </div>
        );
    }
}
