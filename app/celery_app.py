import asyncio
from traceback import format_exc

from celery import Celery
from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient

app = Celery('tasks', broker=f'{config.REDIS_URL}/1')


async def _initialize_offer(offer_id: int):
    offer = await Offer.get_by_id(offer_id)
    client = BitPapaClient(token=config.BITPAPA_TOKEN)
    try:
        offer_data = await client.get_offer_by_number(offer.number)
    except Exception as e:
        await offer.update(
            init_error=format_exc(),
            is_initialized=False
        )
        return

    await offer.update(
        crypto_currency_code=offer_data.crypto_currency_code,
        currency_code=offer_data.currency_code,
        is_initialized=True,
        init_error=None
    )


@app.task
def initialize_offer(offer_id: int):
    asyncio.get_event_loop().run_until_complete(_initialize_offer(offer_id))
