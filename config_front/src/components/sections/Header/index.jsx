import React from "react";
import "./index.scss";
import {useRecoilState} from "recoil";
import {userAtom} from "../../../recoil/atoms";

export default () => {
    const [currentUser, setCurrentUser] = useRecoilState(userAtom);

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        window.location.href = "/login";
    }

    return (
        <div className="header">
            {currentUser ? (
                <>
                    <a className="header__home" href="/">bitpapa bot</a>
                    <button className="header__logout" onClick={logout}>Logout</button>
                </>
            ) : null}
        </div>
    )
}