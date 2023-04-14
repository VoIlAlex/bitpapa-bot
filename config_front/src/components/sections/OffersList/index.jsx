import React, {useEffect, useState} from "react";
import "./index.scss";
import {compileRequest} from "../../../requests/base";
import {requestDeleteOffer, requestOffers} from "../../../requests/offers";
import classNames from "classnames";


export default ({className}) => {
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
                    alert(`An error occurred while trying to delete an offer: ${err}`)
                }
            )
        }
    }

    return (
        <div className={classNames(className, "offers-list")}>
            <h1 className="offers-list__title">Your offers</h1>
            <div className="offers-list__list">
                {offers ? (
                    offers.map(offer => (
                        <div className="offers-list__list-item">
                            <a className="offers-list__list-item-link" href={"/offers/" + offer.id}>
                                <div className="offers-list__list-item-container">
                                    <p className="offers-list__list-item-text">{offer.number}</p>
                                </div>
                            </a>
                            <button className="offers-list__list-item-delete" onClick={() => deleteOffer(offer)}>Delete</button>
                        </div>

                    ))
                ) : null}
            </div>
            <a className="offers-list__create-button" href="/offers/new">Create</a>
        </div>
    )
}
