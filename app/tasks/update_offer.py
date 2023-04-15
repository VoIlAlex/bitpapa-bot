import asyncio
from traceback import print_exc

from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient


class TaskUpdateOffer:
    @staticmethod
    async def update_offer_price(offer):
        client = BitPapaClient(
            token=config.BITPAPA_TOKEN
        )
        if offer.current_min_price:
            if offer.current_price is None or offer.current_price != offer.current_min_price:
                await client.update_offer(offer.number, offer.current_min_price)
                await offer.update(
                    current_price=offer.current_min_price
                )

    @staticmethod
    async def update_offer_prices():
        offers = await Offer.get_all_active()
        tasks = [
            TaskUpdateOffer.update_offer_price(offer)
            for offer in offers
        ]
        await asyncio.gather(*tasks, return_exceptions=False)

    @staticmethod
    def start_loop():
        while True:
            try:
                asyncio.get_event_loop().run_until_complete(
                    TaskUpdateOffer.update_offer_prices()
                )
            except Exception:
                print_exc()
