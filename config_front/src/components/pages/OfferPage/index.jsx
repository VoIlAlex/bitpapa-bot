import React from "react";
import "./index.scss";
import {useParams} from "react-router-dom";
import Header from "../../sections/Header";
import OfferForm from "../../sections/OfferForm";
import {Helmet} from "react-helmet";
import Footer from "../../sections/Footer";

export default () => {
    const { offerId } = useParams();

    return (
        <div className="offer-page">
            <Helmet>
                <meta charSet="utf-8" />
                <title>{offerId === "new" ? "New offer" : `Offer #${offerId}`} | Bitpapa BOT</title>
            </Helmet>
            <Header />
            <div className="offer-page__form-container">
                <OfferForm className="offer-page__form" offerId={offerId}/>
            </div>
            <Footer />
        </div>
    )
}