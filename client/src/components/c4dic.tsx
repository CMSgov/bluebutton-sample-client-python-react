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
    coverageClass: string,
    contractId: string,
    coverageStartDate: string,
    coverageActive: string,
    referenceYear: string,
}

export type InsuranceInfo = {
    fullName: string,
    gender: string,
    dob: string,
    identifier: string, // mbi
    relationship: string, // self, spouse etc.
    coverages: CoverageInfo[] // Part A, Part B, Part C, Part D
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
                if (insuranceData.insInfo) {
                    const coverages: CoverageInfo[] = insuranceData.insInfo.coverages.map((coverage: any) => {
                        return {
                            coverageClass: coverage.class,
                            contractId: coverage.contractId,
                            coverageStartDate: coverage.startDate,
                            coverageActive: coverage.isActive,
                            referenceYear: coverage.referenceYear}
                    });
                    setInsInfo(
                        {
                            fullName: insuranceData.insInfo.fullName,
                            gender: insuranceData.insInfo.gender,
                            dob: insuranceData.insInfo.dob,
                            identifier: insuranceData.insInfo.identifier,
                            relationship: insuranceData.insInfo.relationship,
                            coverages: coverages
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
                    <pre>{insInfo?.fullName||"Null"}    {insInfo?.gender||"Null"}    {insInfo?.dob||"Null"}</pre>
                    <pre>MBI: {insInfo?.identifier||"Null"}</pre>
                    <pre>Relationship to insured: {insInfo?.relationship||"Null"}</pre>

                    {insInfo?.coverages.map(cvrg => {
                            return (
                                <div>
                                    <pre>Coverage Type: {cvrg.coverageClass}</pre>
                                    <pre>Contract Number: {cvrg.contractId}</pre>
                                    <pre>Start Date: {cvrg.coverageStartDate}</pre>
                                    <pre>Active: {cvrg.coverageActive}</pre>
                                    <pre>Reference Year: {cvrg.referenceYear}</pre>
                                </div>
                            )
                        })}
                </div>
            </div>
        );
    }
}
