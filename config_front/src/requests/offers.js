import {OFFERS_URL, TOKEN_URL} from "../config";

export const requestOffers = (token) => {
    return fetch(OFFERS_URL, {
        headers: {
            "Authorization": "Bearer " + token,
        }
    })
}

export const requestOfferById = (token, id) => {
    return fetch(`${OFFERS_URL}${id}/`, {
        headers: {
            "Authorization": "Bearer " + token
        }
    })
}

export const requestUpdateOffer = (token, offerId, data) => {
    return fetch(`${OFFERS_URL}${offerId}/`, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
    })
}

export const requestCreateOffer = (token, data) => {
    return fetch(`${OFFERS_URL}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
        }
    })
}