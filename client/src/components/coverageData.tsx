import React, {useEffect, useState} from 'react';
import {ErrorResponse} from "./records";

export type INScard = {
    ins_name: string;
    plan: string;
    mbi: string;
    date_a: string;
    type: string;
    group: string;
}

export default function CoverageData() {

    const [card, setCard] = useState<INScard>();
    const [message, setMessage] = useState<ErrorResponse>();

    useEffect(() => {
        fetch('/api/data/insurance')
            .then(res => {
                return res.json();
            }).then(insData => {
            if (insData) {
                let card: INScard =
                {
                    ins_name: insData['patient_name'],
                    plan: insData['plan'],
                    mbi: insData['mbi'],
                    date_a: insData['date_a'],
                    type: insData['type'],
                    group: insData['group']
                }
                setCard(card);
            }
            else {
                if (insData) {
                    setMessage({"type": "error", "content": insData.message || "Unknown"})
                }
            }
        });
    });

    if(card) {
        return (
            <div>
                <h2 style={{ textDecoration: 'none', color: 'green' }}>Medicare Coverage Data</h2>
                <div className='ds-u-display--flex ds-u-flex-direction--column ds-u-align-items--center'>
                    <p><b>Subscriber:</b> {card.ins_name}</p>
                    <p><b>Plan:</b> {card.plan}</p>
                    <p><b>Member ID:</b> {card.mbi}</p>
                    <p><b>Start Date:</b> {card.date_a}</p>
                    <p><b>Type:</b> {card.type}</p>
                    <p><b>Group:</b> {card.group}</p>
                </div>
            </div>
        );
    } else {
        return (
            <div>
                <h3>Medicare Data</h3>
                <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start"/>
            </div>
        );
    }
}