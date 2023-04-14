import React from "react";
import "./index.scss";
import Header from "../../sections/Header";
import LoginForm from "../../sections/LoginForm";


export default () => {
    return (
        <div className="login-page">
            <Header />
            <LoginForm className="login-page__form" />
        </div>
    )
}
