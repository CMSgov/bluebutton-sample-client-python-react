import { Badge } from '@cmsgov/design-system';
import React from 'react'

export default function Header() {
   return (
        <header className="ds-u-padding--3 ds-u-sm-padding--6 ds-u-display--block ds-u-fill--primary-darkest">
            <h1 className="ds-u-margin--0 ds-u-color--white ds-u-font-size--5xl ds-u-text-align--center">
                    Blue Button 2.0 Sample App
            </h1>
            <div className="ds-u-text-align--center">
                <Badge variation="info" size="big">
                    Medicare Prescription Drug Claims Data
                </Badge>
            </div>
        </header>
   );
}
