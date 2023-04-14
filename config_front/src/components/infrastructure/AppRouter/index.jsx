import React from "react";
import {createBrowserRouter} from "react-router-dom";
import HomePage from "../../pages/HomePage";
import LoginPage from "../../pages/LoginPage";
import OfferPage from "../../pages/OfferPage";


export const router = createBrowserRouter([
    {
        path: "/",
        element: <HomePage />
    },
    {
        path: "/login",
        element: <LoginPage />
    },
    {
        path: "/offers/:offerId",
        element: <OfferPage />
    }
])
