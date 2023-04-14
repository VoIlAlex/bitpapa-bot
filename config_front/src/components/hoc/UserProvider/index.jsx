import React, {useEffect} from "react";
import "./index.scss";
import {useRecoilState} from "recoil";
import {userAtom} from "../../../recoil/atoms";
import {useLocation} from "react-router-dom";
import {compileRequest} from "../../../requests/base";
import {requestMe} from "../../../requests/auth";
import {
    CircleLoader,
    ClipLoader,
    MoonLoader,
    PacmanLoader,
    PropagateLoader,
    RingLoader,
    ScaleLoader
} from "react-spinners";


export default ({children}) => {

    const [currentUser, setCurrentUser] = useRecoilState(userAtom);

    useEffect(() => {
        if (window.location.pathname !== "/login") {
            const accessToken = localStorage.getItem("access_token");
            if (accessToken) {
                compileRequest(
                    () => {
                        const accessToken = localStorage.getItem("access_token");
                        return requestMe(accessToken)
                    },
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
        return (
            <div className="user-hoc">
                <div className="user-hoc__spinner-container">
                    <h1 className="user-hoc__spinner-text">Retrieving user</h1>
                    <div className="user-hoc__spinner-wrapper">
                        <ScaleLoader
                            color={"#f5f7fa"}
                            loading={true}
                            height={30}
                            aria-label="Loading Spinner"
                            data-testid="loader"
                        />
                    </div>
                </div>
            </div>
        )
    }
}