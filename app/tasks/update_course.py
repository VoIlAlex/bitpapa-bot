import asyncio
from logging import getLogger
from typing import List

from config import config
from db.models import Offer
from db.models.courses import Course
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import ExchangeRate
from tasks.base import Task


logger = getLogger(__name__)


class TaskUpdateCourse(Task):
    @staticmethod
    async def update_course_data(courses_list: List[ExchangeRate], crypto_currency_code: str, currency_code: str):
        if crypto_currency_code and currency_code:
            for exchange_rate in courses_list:
                if (
                    exchange_rate.crypto_currency_code == crypto_currency_code
                    and exchange_rate.currency_code == currency_code
                ):
                    await Course.update_data(
                        currency_code=currency_code,
                        crypto_currency_code=crypto_currency_code,
                        price=exchange_rate.price
                    )
                    break

    @staticmethod
    async def execute(crypto_currency_code: str = None, currency_code: str = None):
        if not crypto_currency_code and not currency_code:
            offers = await Offer.get_all_active()
            logger.info(f"Offers to process: {', '.join(str(offer.id) for offer in offers)}")
            currencies_to_update = set([(o.crypto_currency_code, o.currency_code) for o in offers])
        else:
            currencies_to_update = [(crypto_currency_code, currency_code)]
        bitpapa_client = BitPapaClient(token=config.BITPAPA_TOKEN)
        courses_list = await bitpapa_client.get_exchange_rates()
        tasks = [
            TaskUpdateCourse.update_course_data(
                courses_list=courses_list,
                crypto_currency_code=c[0],
                currency_code=c[1],
            ) for c in currencies_to_update
        ]
        await asyncio.gather(*tasks, return_exceptions=False)
