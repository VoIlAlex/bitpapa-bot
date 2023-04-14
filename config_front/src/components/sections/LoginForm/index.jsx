import React, {useState} from "react";
import "./index.scss";
import {compileRequest} from "../../../requests/base";
import {requestToken} from "../../../requests/auth";
import classNames from "classnames";


export default ({className}) => {
    const [username, setUsername] = useState();
    const [password, setPassword] = useState();

    const login = (e) => {
        e.preventDefault();
        compileRequest(
            () => requestToken(username, password),
            data => {
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("refresh_token", data.refresh_token);
                window.location.href = "/";
            },
            err => {
                alert("Wrong username or password.");
                setPassword("");
            }
        )
    }

    return (
        <form className={classNames(className, "login-form")} onSubmit={login}>
            <h1 className="login-form__title">Login</h1>
            <input
                placeholder={"Username"}
                className="login-form__input"
                value={username}
                onChange={e => setUsername(e.target.value)}
            />
            <input
                placeholder={"Password"}
                className="login-form__input"
                type={"password"}
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <button className="login-form__submit" type={"submit"}>Login</button>
        </form>
    )
}
