import React, {useState} from "react";
import {compileRequest} from "../../../requests/base";
import {requestToken} from "../../../requests/auth";


export default () => {
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
            err => setPassword("")
        )
    }

    return (
        <div>
            <form onSubmit={login}>
                <input value={username} onChange={e => setUsername(e.target.value)} />
                <input value={password} onChange={e => setPassword(e.target.value)} />
                <button type={"submit"}>Login</button>
            </form>
        </div>
    )
}
