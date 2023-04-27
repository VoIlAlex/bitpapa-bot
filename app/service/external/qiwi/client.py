from datetime import datetime
from logging import getLogger
from typing import Union, Dict, Optional
from decimal import Decimal

import httpx

from service.external.qiwi.schema import Bill

logger = getLogger(__name__)


class QiwiClient:
    def __init__(self, token: str, qiwi_api_url: str = "'https://api.qiwi.com"):
        self.token = token
        self.qiwi_api_url = qiwi_api_url

    async def create_bill(
        self,
        site_id: str,
        bill_id: str,
        amount_value: Union[Decimal, float, str],
        amount_currency: str,
        comment: str,
        expiration_date_time: datetime,
        customer_phone: str,
        customer_email: Optional[str],
        customer_account: Optional[str],
        custom_fields: Dict[str, str]
    ) -> Bill:
        url = f'{self.qiwi_api_url}/partner/bill/v1/bills/{bill_id}'
        body = {
            "site_id": site_id,
            "amount": {
                "currency": amount_currency,
                "value": amount_value
            },
            "comment": comment,
            "expirationDateTime": expiration_date_time,
            "customer": {
                "phone": customer_phone,
                "email": customer_email,
                "account": customer_account
            },
            "customFields": custom_fields
        }

        async with httpx.AsyncClient() as client:
            res = await client.put(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}"
                },
                json=body
            )

            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}

                logger.error("Error while handling request on creating bill.")
                raise RuntimeError("Error while request.", res.status_code, err_info)

            return Bill(**res.json())

    async def get_bill(self, bill_id: str):
        url = f'{self.qiwi_api_url}/partner/bill/v1/bills/{bill_id}'

        async with httpx.AsyncClient() as client:
            res = await client.get(
                url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.token}"
                },
            )

            if res.status_code != 200:
                try:
                    err_info = res.json()
                except Exception:
                    err_info = {}

                logger.error("Error while handling request on creating bill.")
                raise RuntimeError("Error while request.", res.status_code, err_info)

            return Bill(**res.json())
