import asyncio
from logging import getLogger

from config import config
from db.models import Trade
from service.external.bitpapa.client import BitPapaClient
from service.external.qiwi.client import QiwiClient
from service.trade_bot.bot import TradeBot
from tasks.base import Task


logger = getLogger(__name__)


class TaskHandleTrade(Task):
    @staticmethod
    async def execute():
        client = BitPapaClient(config.BITPAPA_TOKEN)
        trade_ids = await Trade.get_active_external_ids()
        qiwi_client = QiwiClient(token=config.QIWI_TOKEN)
        bots = [TradeBot(
            bitpapa_client=client,
            qiwi_client=qiwi_client,
            trade_id=trade_id,
            offer_id=offer_id
        ) for trade_id, offer_id in trade_ids]
        await asyncio.gather(*[bot.process() for bot in bots])
