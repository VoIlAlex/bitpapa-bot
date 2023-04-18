import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Union

from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import SearchOffer
from tasks.base import Task


class TaskUpdatePriceInfo(Task):
    @staticmethod
    def check_offer_params(
        offer_data: SearchOffer,
        price_limit_max: Union[Decimal, float],
        price_limit_min: Union[Decimal, float],
        minutes_offline_max: int
    ):
        if price_limit_min > offer_data.price < price_limit_max:
            return False
        if not offer_data.user.online:
            minutes_offline = (
                datetime.utcnow() - offer_data.user.last_sign_in_at
            ).seconds / 60.0
            if minutes_offline > minutes_offline_max:
                return False
        return True

    @staticmethod
    async def update_price_info_for_offer(offer: Offer):
        client = BitPapaClient(
            token=config.BITPAPA_TOKEN
        )
        pages = -1
        page = 0

        while pages == -1 or page <= pages:
            results = await client.search(
                crypto_currency_code=offer.crypto_currency_code,
                type_="Ad::Sell",
                currency_code=offer.currency_code,
                page=page
            )
            pages = results.pages
            page += 1

            for ad in results.ads:
                ad_match = TaskUpdatePriceInfo.check_offer_params(
                    offer_data=ad,
                    price_limit_min=offer.search_price_limit_min,
                    price_limit_max=offer.search_price_limit_max,
                    minutes_offline_max=offer.search_minutes_offline_max
                )
                if ad_match:
                    await offer.update(
                        current_min_price=ad.price
                    )

    @staticmethod
    async def execute():
        offers = await Offer.get_all_active()
        tasks = [
            TaskUpdatePriceInfo.update_price_info_for_offer(offer)
            for offer in offers
        ]
        await asyncio.gather(*tasks, return_exceptions=False)
