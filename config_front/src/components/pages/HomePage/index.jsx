import React, {useEffect, useState} from "react";
import {compileRequest} from "../../../requests/base";
import {requestDeleteOffer, requestOffers} from "../../../requests/offers";
import Header from "../../sections/Header";


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

    const deleteOffer = (offer) => {
        const verification = window.confirm(`Are you sure you want to delete offer with number ${offer.number}`);
        if (verification) {
            compileRequest(
                () => {
                    const accessToken = localStorage.getItem("access_token");
                    return requestDeleteOffer(accessToken, offer.id);
                },
                data => {
                    window.location.reload();
                },
                err => {
                    alert("An error occurred while trying to delete an offer.")
                }
            )
        }
    }

    return (
        <div className="home-page">
            <Header />
            <div className="home-page__offers-list">
                {offers ? (
                    offers.map(offer => (
                        <div>
                            <a href={"/offers/" + offer.id}>
                                <div>
                                    <p>{offer.number}</p>
                                </div>
                            </a>
                            <button onClick={() => deleteOffer(offer)}>Delete</button>
                        </div>

                    ))
                ) : null}
            </div>
            <a href="/offers/new">Create</a>
        </div>
    )
}
