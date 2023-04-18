import asyncio
import json
import redis.asyncio as redis
from datetime import datetime, timezone
from decimal import Decimal
from logging import getLogger
from typing import Union

from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import SearchOffer
from tasks.base import Task


logger = getLogger(__name__)


class TaskUpdatePriceInfo(Task):
    @staticmethod
    def check_offer_params(
        offer_data: SearchOffer,
        price_limit_max: Union[Decimal, float],
        price_limit_min: Union[Decimal, float],
        minutes_offline_max: int
    ):
        if offer_data.price < price_limit_min:
            logger.info(f"Min: {price_limit_min} Current: {offer_data.price}")
            return False
        if offer_data.price > price_limit_max:
            logger.info(f"Max: {price_limit_max} Current: {offer_data.price}")
            return False
        if not offer_data.user.online:
            minutes_offline = (
                datetime.now(timezone.utc) - offer_data.user.last_sign_in_at
            ).seconds / 60.0
            if minutes_offline > minutes_offline_max:
                logger.info(f"Max minutes offline: {minutes_offline_max} Minutes offline: {minutes_offline}")
                return False
        return True

    @staticmethod
    async def send_websocket_message(offer_id: int, price: str):
        r = redis.from_url(config.REDIS_URL)
        channel_name = f"offer-channel:{offer_id}"
        await r.publish(channel_name, json.dumps({
            "type": "update-min-price",
            "data": {
                "offer_id": offer_id,
                "price": price
            }
        }))

    @staticmethod
    async def update_price_info_for_offer(offer: Offer):
        client = BitPapaClient(
            token=config.BITPAPA_TOKEN
        )
        pages = -1
        page = 0

        while pages == -1 or page <= pages:
            now = datetime.now()
            results = await client.search(
                crypto_currency_code=offer.crypto_currency_code,
                type_="Ad::Sell",
                currency_code=offer.currency_code,
                page=page
            )
            spent_time = datetime.now() - now
            logger.info(f"Request complete in {spent_time.seconds}.{spent_time.microseconds} seconds.")
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
                    if offer.current_min_price is None or offer.current_min_price != ad.price:
                        await offer.update(
                            current_min_price=ad.price
                        )
                        await TaskUpdatePriceInfo.send_websocket_message(offer.id, ad.price)
                        return

    @staticmethod
    async def execute():
        offers = await Offer.get_all_active()
        logger.info(f"Offers to process: {', '.join(str(offer.id) for offer in offers)}")
        tasks = [
            TaskUpdatePriceInfo.update_price_info_for_offer(offer)
            for offer in offers
        ]
        await asyncio.gather(*tasks, return_exceptions=False)
