import React from "react";
import "./index.scss";
import Header from "../../sections/Header";
import OffersList from "../../sections/OffersList";
import {Helmet} from "react-helmet";
import Footer from "../../sections/Footer";


export default () => {
    return (
        <div className="home-page">
            <Helmet>
                <meta charSet="utf-8" />
                <title>Home | Bitpapa BOT</title>
            </Helmet>
            <Header />
            <OffersList className="home-page__offers-list" />
            <Footer />
        </div>
    )
}
