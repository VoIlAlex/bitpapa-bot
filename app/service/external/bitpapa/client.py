import base64
import json
import logging
import os.path
from decimal import Decimal
from typing import Union, Optional, List

import httpx

from service.external.bitpapa.schema import SearchOffersResult, SearchOffer, TradeConversation, \
    TradeConversationMessage, Trade, ExchangeRate, TradeConversationMessageSent

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
    ) -> SearchOffersResult:
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
            "equation": price
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

    async def get_offer_by_number(
        self,
        number: str
    ) -> SearchOffer:
        url = f'{self.api_url}/pro/{number}'
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                headers={
                    "X-Access-Token": self.token
                },
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

            return SearchOffer(**res.json()["ad"])

    async def cancel_trade(self, trade_id: str):
        url = f'{self.api_url}/trades/{trade_id}/cancel'
        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

    async def complete_trade(self, trade_id: str):
        url = f'{self.api_url}/trades/{trade_id}/complete'

        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

    async def get_trade_conversation(
        self,
        trade_id: str
    ) -> TradeConversation:
        url = f'{self.api_url}/trades/{trade_id}/trade_conversation'

        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)
        return TradeConversation(**res.json())

    async def create_message_in_trade_conversation(
        self,
        trade_id: str,
        body: str,
        file_path: Optional[str] = None
    ):
        url = f'{self.api_url}/trades/{trade_id}/create_message_in_trade_conversation'

        request_body = {
            "body": body
        }

        if file_path:
            filename = os.path.split(file_path)[-1]
            with open(file_path, 'rb') as f:
                encoded_file = base64.b64encode(f.read())

            request_body["filename"] = filename
            request_body["attachment"] = encoded_file

        async with httpx.AsyncClient() as client:
            res = await client.post(
                url,
                headers={
                    "X-Access-Token": self.token,
                    "Content-Type": "application/json"
                },
                json=request_body
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)
            return TradeConversationMessage(**res.json()["message"])

    async def get_trade(
        self,
        trade_id: str
    ) -> Trade:
        url = f'{self.api_url}/trades/{trade_id}'
        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

        return Trade(**res.json()["trade"])

    async def list_latest_trades(self) -> List[Trade]:
        url = f'{self.api_url}/trades'

        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                params={
                    'limit': 500,
                    # 'type': 'buy',  # TODO: check correct type
                    # 'status': 'opened',  # TODO: check correct status
                    'sort': '-created_at'
                },
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

        return [Trade(**trade_data) for trade_data in res.json()["trades"]]

    async def get_exchange_rates(self) -> List[ExchangeRate]:
        url = f'{self.api_url}/exchange_rates/all'

        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                headers={
                    "X-Access-Token": self.token
                }
            )
            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}
                raise RuntimeError("Request error.", res.status_code, err_info)

        rates = []

        data = res.json()
        for rate_key, rate_value in data["rates"].items():
            crypto_currency_code, currency_code = rate_key.split("_")
            rates.append(ExchangeRate(
                crypto_currency_code=crypto_currency_code,
                currency_code=currency_code,
                price=rate_value
            ))

        return rates
