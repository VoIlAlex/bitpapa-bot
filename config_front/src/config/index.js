export const API_URL = process.env.REACT_APP_API_URL ? process.env.REACT_APP_API_URL : "http://localhost:8555/api/v1";
export const ME_URL = API_URL + "/auth/me/";
export const TOKEN_URL = API_URL + "/auth/token/";
export const TOKEN_REFRESH_URL = API_URL + "/auth/token/refresh/";
export const OFFERS_URL = API_URL + "/offers/";