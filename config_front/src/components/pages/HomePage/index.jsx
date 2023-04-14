import React from "react";
import "./index.scss";
import Header from "../../sections/Header";
import OffersList from "../../sections/OffersList";


export default () => {
    return (
        <div className="home-page">
            <Header />
            <OffersList className="home-page__offers-list" />
        </div>
    )
}
