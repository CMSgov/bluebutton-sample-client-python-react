import React, {useEffect, useState} from 'react';
import {ErrorResponse} from "./records";


export type INScard = {
    ins_name: string;
    mbi: string;
    date_a: string;
    date_b: string;
}
export default function InsuranceCardData() {

    const [card, setCard] = useState<INScard>();
    const [message, setMessage] = useState<ErrorResponse>();

    useEffect(() => {
        fetch('/api/data/insurance')
            .then(res => {
                return res.json();
            }).then(insData => {
            if (insData.card) {
                let card: INScard =
                {
                    ins_name: insData['patient_name'],
                    mbi: insData['mbi'],
                    date_a: insData['date_a'],
                    date_b: insData['date_b']
                }
                setCard(card);
            }
            else {
                if (insData.message) {
                    setMessage({"type": "error", "content": insData.message || "Unknown"})
                }
            }
        });
    });

    if(card) {
        return (
            <div>
                <h3>Medicare Digital Insurance Card</h3>
                <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start background">
                    <div className="name">{card.ins_name}</div>
                    <div className="mbi">{card.mbi}</div>
                    <div className="date-a">{card.date_a}</div>
                    <div className="date-b">{card.date_b}</div>
                </div>
            </div>
        );
    } else {
        return (
            <div>
                <h3>Medicare Digital Insurance Card</h3>
                <div className="ds-u-display--flex ds-u-flex-direction--row ds-u-align-items--start background"/>
            </div>
        );
    }
}