import {OFFERS_URL, TOKEN_URL} from "../config";

export const requestOffers = (token) => {
    return fetch(OFFERS_URL, {
        headers: {
            "Authorization": "Bearer " + token,
        }
    })
}