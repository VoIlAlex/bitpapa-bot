import React, {useEffect, useState} from "react";
import "./index.scss";
import {requestCreateOffer, requestOfferById, requestUpdateOffer} from "../../../requests/offers";
import {useParams} from "react-router-dom";
import {compileRequest} from "../../../requests/base";
import Header from "../../sections/Header";
import classNames from "classnames";

export default ({offerId, className}) => {
    const [offer, setOffer] = useState(null);

    useEffect(() => {
        if (offerId !== "new") {
            compileRequest(
                () => {
                    const token = localStorage.getItem("access_token");
                    return requestOfferById(token, offerId);
                },
                data => setOffer(data)
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
                search_minutes_offline_max: "0"
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
            <button className="offer-form__save-button" type={"submit"}>{offerId === "new" ? "Create" : "Update"}</button>
        </form>
    ) : null
}