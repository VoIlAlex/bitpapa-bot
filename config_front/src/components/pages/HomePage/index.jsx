import React, {useEffect, useState} from "react";
import {compileRequest} from "../../../requests/base";
import {requestOffers} from "../../../requests/offers";


export default () => {
    const [offers, setOffers] = useState(null);

    useEffect(() => {
        compileRequest(
            () => {
                const accessToken = localStorage.getItem("access_token");
                return requestOffers(accessToken)
            },
            data => setOffers(data)
        )
    }, [])

    return (
        <div className="home-page">
            <div className="home-page__offers-list">
                {offers ? (
                    offers.map(offer => (
                        <a href={"/offers/" + offer.id}>
                            <div>
                                <p>{offer.number}</p>
                            </div>
                        </a>
                    ))
                ) : null}
            </div>
        </div>
    )
}
