import React from "react";
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
        <div>
            {currentUser ? (
                <>
                    <a href="/">Home</a>
                    <button onClick={logout}>Logout</button>
                </>
            ) : null}
        </div>
    )
}