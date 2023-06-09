import asyncio
from traceback import format_exc

from celery import Celery
from config import config
from db.models import Offer
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import OfferType
from tasks.update_course import TaskUpdateCourse

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

    if offer_data.payment_method_code not in config.ALLOWED_PAYMENT_METHOD_CODES:
        await offer.update(
            init_error=(
                f"Payment method should be in {config.ALLOWED_PAYMENT_METHOD_CODES}. "
                f"Got \"{offer_data.payment_method_code}\""
            ),
            is_initialized=False
        )
        return

    if offer_data.type != OfferType.SELL.value:
        await offer.update(
            init_error=(
                f"Offer type should be \"{OfferType.SELL.value}\". "
                f"Got \"{offer_data.type}\""
            ),
            is_initialized=False
        )
        return

    await TaskUpdateCourse.execute(
        crypto_currency_code=offer_data.crypto_currency_code,
        currency_code=offer_data.crypto_currency_code
    )
    await offer.update(
        crypto_currency_code=offer_data.crypto_currency_code,
        currency_code=offer_data.currency_code,
        user_id=offer_data.user.id,
        user_name=offer_data.user.user_name,
        is_initialized=True,
        init_error=None
    )


@app.task
def initialize_offer(offer_id: int):
    asyncio.get_event_loop().run_until_complete(_initialize_offer(offer_id))
