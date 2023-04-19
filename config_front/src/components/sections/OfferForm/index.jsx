import React, {useEffect, useState} from "react";
import "./index.scss";
import {requestCreateOffer, requestOfferById, requestUpdateOffer} from "../../../requests/offers";
import {useParams} from "react-router-dom";
import {compileRequest} from "../../../requests/base";
import Header from "../../sections/Header";
import classNames from "classnames";
import {OFFERS_URL} from "../../../config";

export default ({offerId, className}) => {
    const [offer, setOffer] = useState(null);
    const [websocket, setWebsocket] = useState(null);

    const [currentMinPriceExtra, setCurrentMinPriceExtra] = useState(false);
    const [currentMinPrice, setCurrentMinPrice] = useState(null);
    const [currentMinPriceFound, setCurrentMinPriceFound] = useState(null);
    const [currentMinPriceLastResponseDuration, setCurrentMinPriceLastResponseDuration] = useState(null);
    const [currentMinPriceLastUpdated, setCurrentMinPriceLastUpdated] = useState(null);
    const [currentMinPriceRequestsNumber, setCurrentMinPriceRequestsNumber] = useState(null);
    const [currentMinPriceTotalDuration, setCurrentMinPriceTotalDuration] = useState(null);

    const formatTime = (timestr) => {
        if (timestr) {
            const date = new Date(timestr);
            return date.toUTCString();
        }
        return null;
    }

    useEffect(() => {
        if (offerId !== "new" && !websocket) {
            let url = new URL(`${OFFERS_URL}${offerId}/websocket/`);
            // TODO: Add secure connection (token)
            url.protocol = url.protocol === "https:" ? "wss" : "ws";
            const ws = new WebSocket(url)
            setWebsocket(ws);
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.type === "update-min-price") {
                    const price = data.data.price ? data.data.price.toFixed(2) : null;
                    const found = data.data.found;
                    const lastResponseDuration = data.data.last_response_duration;
                    const lastUpdated = data.data.last_updated;
                    const requestsNumber = data.data.requests_number;
                    const totalDuration = data.data.total_duration;

                    setCurrentMinPrice(price);
                    setCurrentMinPriceFound(found);
                    setCurrentMinPriceLastResponseDuration(lastResponseDuration);
                    setCurrentMinPriceLastUpdated(formatTime(lastUpdated));
                    setCurrentMinPriceRequestsNumber(requestsNumber);
                    setCurrentMinPriceTotalDuration(totalDuration);
                }
            }
        }
    }, [offerId, websocket])

    useEffect(() => {
        if (offerId !== "new") {
            compileRequest(
                () => {
                    const token = localStorage.getItem("access_token");
                    return requestOfferById(token, offerId);
                },
                data => {
                    setOffer(data)
                    setCurrentMinPrice(data.current_min_price.toFixed(2));
                    setCurrentMinPriceRequestsNumber(data.current_min_price_requests_number);
                    setCurrentMinPriceFound(data.current_min_price_found);
                    setCurrentMinPriceLastResponseDuration(data.current_min_price_last_response_duration);
                    setCurrentMinPriceTotalDuration(data.current_min_price_total_duration);
                    setCurrentMinPriceLastUpdated(formatTime(data.current_min_price_last_updated));
                }
            )

        } else {
            setOffer({
                number: "",
                min_price: "0",
                beat_price_by: "0",
                greeting_only: true,
                auto_trade_close: true,
                search_price_limit_min: "0",
                search_price_limit_max: "0",
                search_minutes_offline_max: "0",
                is_active: true
            })
        }
    }, [offerId])

    const onFormSave = (e) => {
        e.preventDefault()
        if (offerId === "new") {
            compileRequest(
                () => {
                    const accessToken = localStorage.getItem("access_token");
                    return requestCreateOffer(accessToken, offer)
                },
                data => {
                    window.location.href = "/"
                },
                err => {
                    alert(`Error creating order: ${err}`)
                }
            )
        } else {
            compileRequest(
                () => {
                    const accessToken = localStorage.getItem("access_token");
                    return requestUpdateOffer(accessToken, offerId, offer)
                },
                data => {
                    window.location.reload()
                },
                err => {
                    alert(`Error updating order: ${err}`)
                }
            )
        }
    }

    return offer ? (
        <form className={classNames(className, "offer-form")} onSubmit={onFormSave}>
            <h1>{offerId !== "new" ? `Offer #${offerId}` : "New offer"}</h1>
            <label className="offer-form__label" itemID="number">Number:</label>
            <input
                className="offer-form__input"
                id="number"
                value={offer.number}
                onChange={e => setOffer({
                    ...offer,
                    number: e.target.value
                })
            }/>
            <label className="offer-form__label" itemID="min_price">Min price:</label>
            <input
                className="offer-form__input"
                id="min_price"
                value={offer.min_price}
                onChange={e => setOffer({
                    ...offer,
                    min_price: e.target.value
                })
            }/>
            <label className="offer-form__label" itemID="beat_price_by">Beat price by:</label>
            <input
                className="offer-form__input"
                id="beat_price_by"
                value={offer.beat_price_by}
                onChange={e => setOffer({
                    ...offer,
                    beat_price_by: e.target.value
                })
            }/>
            <label className="offer-form__label" itemID="search_price_limit_min">Search price limit min:</label>
            <input
                className="offer-form__input"
                id="search_price_limit_min"
                value={offer.search_price_limit_min}
                onChange={e => setOffer({
                    ...offer,
                    search_price_limit_min: e.target.value
                })
            }/>
            <label className="offer-form__label" itemID="search_price_limit_max">Search price limit max:</label>
            <input
                className="offer-form__input"
                id="search_price_limit_max"
                value={offer.search_price_limit_max}
                onChange={e => setOffer({
                    ...offer,
                    search_price_limit_max: e.target.value
                })
            }/>
            <label className="offer-form__label" itemID="search_minutes_offline_max">Search minutes offline max:</label>
            <input
                className="offer-form__input"
                id="search_minutes_offline_max"
                value={offer.search_minutes_offline_max}
                onChange={e => setOffer({
                    ...offer,
                    search_minutes_offline_max: e.target.value
                })
            }/>
            <div className="offer-form__checkbox-item">
                <label className="offer-form__label" itemID="greeting_only">Greeting only:</label>
                <input
                    className="offer-form__checkbox"
                    id="greeting_only"
                    type={"checkbox"}
                    checked={offer.greeting_only}
                    onChange={e => setOffer({
                        ...offer,
                        greeting_only: e.target.checked
                    })
                }/>
            </div>
            <div className="offer-form__checkbox-item">
                <label className="offer-form__label" itemID="auto_trade_close">Auto trade close:</label>
                <input
                    className="offer-form__checkbox"
                    id="auto_trade_close"
                    type={"checkbox"}
                    checked={offer.auto_trade_close}
                    onChange={e => setOffer({
                        ...offer,
                        auto_trade_close: e.target.checked
                    })
                }/>
            </div>
            <div className="offer-form__checkbox-item">
                <label className="offer-form__label" itemID="is_active">Is active:</label>
                <input
                    className="offer-form__checkbox"
                    id="is_active"
                    type={"checkbox"}
                    checked={offer.is_active}
                    onChange={e => setOffer({
                        ...offer,
                        is_active: e.target.checked
                    })
                }/>
            </div>
            <button className="offer-form__save-button" type={"submit"}>{offerId === "new" ? "Create" : "Update"}</button>
            {offerId !== "new" ? (
                <div className="offer-form__after-button">
                    <p>Price: {offer.current_price}</p>
                    <p>Min price: {currentMinPrice} {offer.currency_code} / {offer.crypto_currency_code}</p>
                    <button type={"button"} onClick={() => {
                        setCurrentMinPriceExtra(!currentMinPriceExtra);
                    }}>Show min price info</button>
                    {currentMinPriceExtra ? (
                        <>
                            <p>Min price (last updated): {currentMinPriceLastUpdated ? currentMinPriceLastUpdated : "-"}</p>
                            <p>Min price (found): {currentMinPriceFound ? "found" : "not found"}</p>
                            <p>Min price (requests number): {currentMinPriceRequestsNumber ? currentMinPriceRequestsNumber : "-"}</p>
                            <p>Min price (total duration): {currentMinPriceTotalDuration ? currentMinPriceTotalDuration / 1000000 : "-"}</p>
                            <p>Min price (last response duration): {currentMinPriceLastResponseDuration ? currentMinPriceLastResponseDuration / 1000000 : "-"}</p>
                        </>
                    ) : null}

                </div>
            ) : null}
        </form>
    ) : null
}