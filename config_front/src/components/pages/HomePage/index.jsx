import React, {useEffect, useState} from "react";
import "./index.scss";
import {compileRequest} from "../../../requests/base";
import {requestDeleteOffer, requestOffers} from "../../../requests/offers";
import Header from "../../sections/Header";
import OffersList from "../../sections/OffersList";


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
            <OffersList className="home-page__offers-list" />
        </div>
    )
}
