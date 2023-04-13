import {ME_URL, TOKEN_URL} from "../config";

export const requestMe = (token) => {
    return fetch(ME_URL, {
        headers: {
            'Authorization': 'Bearer ' + token
        }
    })
}

export const requestToken = (username, password) => {
    return fetch(TOKEN_URL, {
        method: "POST",
        body: JSON.stringify({username, password}),
        headers: {
            "Content-Type": "application/json"
        }
    })
}