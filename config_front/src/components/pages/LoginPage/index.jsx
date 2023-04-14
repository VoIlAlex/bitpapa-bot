import React from "react";
import "./index.scss";
import Header from "../../sections/Header";
import LoginForm from "../../sections/LoginForm";
import {Helmet} from "react-helmet";


export default () => {
    return (
        <div className="login-page">
            <Helmet>
                <meta charSet="utf-8" />
                <title>Login | Bitpapa BOT</title>
            </Helmet>
            <Header />
            <LoginForm className="login-page__form" />
        </div>
    )
}
