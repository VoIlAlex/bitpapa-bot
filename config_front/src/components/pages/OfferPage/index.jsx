import React from "react";
import "./index.scss";
import {useParams} from "react-router-dom";
import Header from "../../sections/Header";
import OfferForm from "../../sections/OfferForm";

export default () => {
    const { offerId } = useParams();

    return (
        <div className="offer-page">
            <Header />
            <OfferForm className="offer-page__form" offerId={offerId}/>
        </div>
    )
}