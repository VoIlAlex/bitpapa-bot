import asyncio
import json
import re
from datetime import datetime, timezone
from traceback import print_exc

import redis.asyncio as redis
from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient
from tasks.base import Task


class TaskUpdateOffer(Task):
    @staticmethod
    def _elapsed_time_microseconds(start_time: datetime):
        now = datetime.now(timezone.utc)
        return int((now - start_time).total_seconds() * 1000000)

    @staticmethod
    async def send_websocket_message(
        offer_id: int,
        price: str,
        total_duration: int = 0,
        last_updated: datetime = None,
        last_request_time: datetime = None,
        last_request_block: int = None
    ):
        r = redis.from_url(config.REDIS_URL)
        channel_name = f"offer-channel:{offer_id}"
        await r.publish(channel_name, json.dumps({
            "type": "update-price",
            "data": {
                "offer_id": offer_id,
                "price": float(price),
                "total_duration": total_duration,
                "last_updated": last_updated.isoformat() if last_updated else None,
                "last_request_time": last_request_time.isoformat() if last_request_block else None,
                "last_request_block": last_request_block
            }
        }))

    @staticmethod
    def _parse_block(err_info: dict) -> int:
        if err_info:
            ad_errors = err_info.get(
                "errors", {}
            ).get(
                "ad", None
            )
            if ad_errors and len(ad_errors) != 0:
                block_err = ad_errors[0]
                pattern = re.compile("in (\d*) sec")
                block_data = pattern.findall(block_err)
                if block_data and len(block_data) != 0:
                    return int(block_data[0])

    @staticmethod
    async def update_offer_price(offer):
        if offer.current_price_last_request_time and offer.current_price_last_request_block:
            time_passed = (datetime.now(timezone.utc) - offer.current_price_last_request_time).total_seconds()
            if time_passed < offer.current_price_last_request_block:
                return

        client = BitPapaClient(
            token=config.BITPAPA_TOKEN
        )
        if offer.current_min_price:
            start_time = datetime.now(timezone.utc)
            price_to_set = max(offer.current_min_price - offer.beat_price_by, offer.min_price)
            if offer.current_price is None or offer.current_price != price_to_set:
                try:
                    await client.update_offer(offer.number, float(price_to_set))
                except RuntimeError as e:
                    try:
                        message, status_code, err_info = e.args
                        block = TaskUpdateOffer._parse_block(err_info)
                        await offer.update(
                            current_price_last_request_time=datetime.now(timezone.utc),
                            current_price_last_request_block=block
                        )
                        await TaskUpdateOffer.send_websocket_message(
                            offer_id=offer.id,
                            price=offer.current_price,
                            total_duration=offer.current_price_total_duration,
                            last_updated=offer.current_price_last_updated,
                            last_request_time=datetime.now(timezone.utc),
                            last_request_block=block
                        )
                    except Exception:
                        print_exc()
                        return
                    return

                if offer.current_price_last_updated:
                    total_duration = TaskUpdateOffer._elapsed_time_microseconds(offer.current_price_last_updated)
                else:
                    total_duration = TaskUpdateOffer._elapsed_time_microseconds(start_time)
                now = datetime.now(timezone.utc)
                await offer.update(
                    current_price=price_to_set,
                    current_price_total_duration=total_duration,
                    current_price_last_request_time=now,
                    current_price_last_request_block=0,
                    current_price_last_updated=now
                )
                await TaskUpdateOffer.send_websocket_message(
                    offer_id=offer.id,
                    price=price_to_set,
                    total_duration=total_duration,
                    last_updated=now,
                    last_request_time=now,
                    last_request_block=0
                )

    @staticmethod
    async def execute():
        offers = await Offer.get_all_active()
        tasks = [
            TaskUpdateOffer.update_offer_price(offer)
            for offer in offers
        ]
        await asyncio.gather(*tasks, return_exceptions=False)
