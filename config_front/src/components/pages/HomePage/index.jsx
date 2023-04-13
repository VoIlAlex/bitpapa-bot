import React, {useEffect, useState} from "react";
import {compileRequest} from "../../../requests/base";
import {requestOffers} from "../../../requests/offers";


export default () => {
    const [offers, setOffers] = useState(null);

    useEffect(() => {
        const accessToken = localStorage.getItem("access_token");
        compileRequest(
            requestOffers(accessToken),
            data => setOffers(data)
        )
    }, [])

    return (
        <div>
            {offers ? (
                offers.map(offer => (
                    <div>
                        <p>{offer.id}</p>
                    </div>
                ))
            ) : null}
        </div>
    )
}
