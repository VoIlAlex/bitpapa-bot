import asyncio
import json
import redis.asyncio as redis
from datetime import datetime, timezone
from decimal import Decimal
from logging import getLogger
from typing import Union, Optional

from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import SearchOffer
from tasks.base import Task


logger = getLogger(__name__)


class TaskUpdatePriceInfo(Task):
    @staticmethod
    def _elapsed_time_microseconds(start_time: datetime):
        now = datetime.now(timezone.utc)
        return int((now - start_time).total_seconds() * 1000000)

    @staticmethod
    def check_offer_params(
        offer_data: SearchOffer,
        price_limit_max: Union[Decimal, float],
        price_limit_min: Union[Decimal, float],
        amount_limit_min: Union[Decimal, float],
        amount_limit_max: Union[Decimal, float],
        minutes_offline_max: int
    ):
        if offer_data.price < price_limit_min:
            logger.info(f"Min: {price_limit_min} Current: {offer_data.price}")
            return False
        if offer_data.price > price_limit_max:
            logger.info(f"Max: {price_limit_max} Current: {offer_data.price}")
            return False
        if offer_data.limit_max > amount_limit_max:
            logger.info(f"Amount max: {amount_limit_max}. Current range: {offer_data.limit_min}-{offer_data.limit_max}")
            return False
        if offer_data.limit_min < amount_limit_min:
            logger.info(f"Amount min: {amount_limit_min}. Current range: {offer_data.limit_min}-{offer_data.limit_max}")
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
    async def send_websocket_message(
        offer_id: int,
        price: str,
        found: bool = False,
        requests_number: int = 1,
        last_response_duration: int = 0,
        total_duration: int = 0,
        last_updated: datetime = None
    ):
        r = redis.from_url(config.REDIS_URL)
        channel_name = f"offer-channel:{offer_id}"
        await r.publish(channel_name, json.dumps({
            "type": "update-min-price",
            "data": {
                "offer_id": offer_id,
                "price": price,
                "found": found,
                "requests_number": requests_number,
                "last_response_duration": last_response_duration,
                "total_duration": total_duration,
                "last_updated": last_updated.isoformat() if last_updated else None
            }
        }))

    @staticmethod
    async def update_price_info_for_offer(offer: Offer):
        client = BitPapaClient(
            token=config.BITPAPA_TOKEN
        )
        pages = -1
        page = 0

        start_time = datetime.now(timezone.utc)
        response_time: Optional[str, None] = None
        min_price_to_set: Optional[str, None] = None

        while pages == -1 or page <= pages:
            iteration_start_time = datetime.now(timezone.utc)
            results = await client.search(
                crypto_currency_code=offer.crypto_currency_code,
                type_="Ad::Sell",
                currency_code=offer.currency_code,
                page=page
            )
            response_time = TaskUpdatePriceInfo._elapsed_time_microseconds(iteration_start_time)
            logger.info(f"Request complete in {response_time / 1000000} seconds.")
            pages = results.pages
            page += 1

            for ad in results.ads:
                ad_match = TaskUpdatePriceInfo.check_offer_params(
                    offer_data=ad,
                    price_limit_min=offer.search_price_limit_min,
                    price_limit_max=offer.search_price_limit_max,
                    amount_limit_min=offer.search_amount_limit_min,
                    amount_limit_max=offer.search_amount_limit_max,
                    minutes_offline_max=offer.search_minutes_offline_max
                )
                if ad_match:
                    if offer.current_min_price is None or offer.current_min_price != ad.price:
                        min_price_to_set = ad.price
                        break

            if min_price_to_set is not None:
                break

        update_fields = {
            "current_min_price_last_updated": datetime.now(timezone.utc),
            "current_min_price_last_response_duration": response_time,
            "current_min_price_total_duration": TaskUpdatePriceInfo._elapsed_time_microseconds(start_time),
            "current_min_price_requests_number": page
        }

        if min_price_to_set is not None:
            update_fields["current_min_price"] = min_price_to_set
            update_fields["current_min_price_found"] = True
        else:
            update_fields["current_min_price_found"] = False

        await offer.update(**update_fields)
        await TaskUpdatePriceInfo.send_websocket_message(
            offer_id=offer.id,
            price=min_price_to_set,
            found=update_fields["current_min_price_found"],
            requests_number=update_fields["current_min_price_requests_number"],
            last_response_duration=update_fields["current_min_price_last_response_duration"],
            total_duration=update_fields["current_min_price_total_duration"],
            last_updated=update_fields["current_min_price_last_updated"]
        )

    @staticmethod
    async def execute():
        offers = await Offer.get_all_active()
        logger.info(f"Offers to process: {', '.join(str(offer.id) for offer in offers)}")
        tasks = [
            TaskUpdatePriceInfo.update_price_info_for_offer(offer)
            for offer in offers
        ]
        await asyncio.gather(*tasks, return_exceptions=False)
