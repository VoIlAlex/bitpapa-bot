import {refreshToken} from "./auth";


export const compileRequest = (requestObjBuilder, outputHandler, errorHandler, autoRefresh = true) => {
    let skip = false;
    requestObjBuilder().then(res => {
        if (res.ok) {
            return res.json()
        } else {
            if (res.status === 401 && autoRefresh) {
                const access_token = localStorage.getItem("access_token");
                const refresh_token = localStorage.getItem("refresh_token");
                if (access_token && refresh_token) {
                    skip = true;
                    compileRequest(
                        () => refreshToken(access_token, refresh_token),
                        data => {
                            console.log("here")
                            localStorage.setItem("access_token", data.access_token);
                            localStorage.setItem("refresh_token", data.refresh_token);
                            compileRequest(requestObjBuilder, outputHandler, errorHandler, false);
                        },
                        err => {
                            console.log("there")
                            localStorage.removeItem("access_token");
                            localStorage.removeItem("refresh_token");
                            window.location.href = "/login";
                        },
                        false
                    )
                }
            }
            throw Error("Error handling request.")
        }
    }).then(
        data => {
            if (skip) {
                return;
            }
            outputHandler(data)
        }
    ).catch(err => {
        if (skip) {
            return;
        }
        if (errorHandler) {
            errorHandler(err);
        }
        console.log(err)
    })
}