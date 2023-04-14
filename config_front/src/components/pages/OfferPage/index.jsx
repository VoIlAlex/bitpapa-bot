import React, {useEffect, useState} from "react";
import {requestCreateOffer, requestOfferById, requestUpdateOffer} from "../../../requests/offers";
import {useParams} from "react-router-dom";
import {compileRequest} from "../../../requests/base";
import Header from "../../sections/Header";

export default () => {
    const [offer, setOffer] = useState(null);
    const { offerId } = useParams();

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
                }
            )
        }
    }

    return (
        <div>
            <Header />
            {offer ? (
                <form onSubmit={onFormSave}>
                    <input
                        value={offer.number}
                        onChange={e => setOffer({
                            ...offer,
                            number: e.target.value
                        })
                    }/>
                    <input
                        value={offer.min_price}
                        onChange={e => setOffer({
                            ...offer,
                            min_price: e.target.value
                        })
                    }/>
                    <input
                        value={offer.beat_price_by}
                        onChange={e => setOffer({
                            ...offer,
                            beat_price_by: e.target.value
                        })
                    }/>
                    <input
                        type={"checkbox"}
                        checked={offer.greeting_only}
                        onChange={e => setOffer({
                            ...offer,
                            greeting_only: e.target.checked
                        })
                    }/>
                    <input
                        type={"checkbox"}
                        checked={offer.auto_trade_close}
                        onChange={e => setOffer({
                            ...offer,
                            auto_trade_close: e.target.checked
                        })
                    }/>
                    <input
                        value={offer.search_price_limit_min}
                        onChange={e => setOffer({
                            ...offer,
                            search_price_limit_min: e.target.value
                        })
                    }/>
                    <input
                        value={offer.search_price_limit_max}
                        onChange={e => setOffer({
                            ...offer,
                            search_price_limit_max: e.target.value
                        })
                    }/>
                    <input
                        value={offer.search_minutes_offline_max}
                        onChange={e => setOffer({
                            ...offer,
                            search_minutes_offline_max: e.target.value
                        })
                    }/>
                    <button type={"submit"}>{offerId === "new" ? "Create" : "Update"}</button>
                </form>
            ) : null}
        </div>
    )
}