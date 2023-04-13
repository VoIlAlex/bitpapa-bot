import React, {useEffect} from "react";
import {useRecoilState} from "recoil";
import {userAtom} from "../../../recoil/atoms";
import {useLocation} from "react-router-dom";
import {compileRequest} from "../../../requests/base";
import {requestMe} from "../../../requests/auth";


export default ({children}) => {
    const [currentUser, setCurrentUser] = useRecoilState(userAtom);

    useEffect(() => {
        const accessToken = localStorage.getItem("access_token");
        if (window.location.pathname !== "/login") {
            if (accessToken) {
                compileRequest(
                    requestMe(accessToken),
                    data => setCurrentUser(data)
                )
            } else {
                window.location.href = "/login";
            }
        }
    }, [])

    if (currentUser || window.location.pathname === "/login") {
        return children;
    } else {
        return "Retrieving user";
    }
}