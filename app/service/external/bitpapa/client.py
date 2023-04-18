import json
import logging
from decimal import Decimal
from typing import Union

import httpx

from service.external.bitpapa.schema import SearchOffersResult


logger = logging.getLogger(__name__)

class BitPapaClient:
    def __init__(self,
                 token: str,
                 api_url: str = "https://bitpapa.com/api/v1"):
        self.token = token
        self.api_url = api_url

    async def search(
        self,
        crypto_currency_code: str = None,
        type_: str = None,
        amount: float = None,
        currency_code: str = None,
        limit: int = 10,
        page: int = 0,
        sort: str = "price"
    ):
        url = f"{self.api_url}/pro/search"
        params = {}
        if crypto_currency_code is not None:
            params["crypto_currency_code"] = crypto_currency_code
        if type_ is not None:
            params["type"] = type_
        if amount is not None:
            params["amount"] = amount
        if currency_code is not None:
            params["currency_code"] = currency_code
        if limit is not None:
            params["limit"] = limit
        if page is not None:
            params["page"] = page
        if sort is not None:
            params["sort"] = sort
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                params=params,
                headers={
                    "Content-Type": "application/json",
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

            data = res.json()
            return SearchOffersResult(**data)

    async def update_offer(
        self,
        offer_id: str,
        price: Union[Decimal, float]
    ):
        url = f"{self.api_url}/pro/{offer_id}"
        body = {
            "price": price
        }
        async with httpx.AsyncClient() as client:
            res = await client.put(
                url,
                headers={
                    "Content-Type": "application/json",
                    "X-Access-Token": self.token
                },
                json=body
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)


