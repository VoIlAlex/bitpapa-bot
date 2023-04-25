import asyncio

from config import config
from service.external.bitpapa.client import BitPapaClient
from service.trade_bot.bot import TradeBot
from tasks.base import Task


class TaskHandleTrade(Task):

    @staticmethod
    async def execute():
        client = BitPapaClient(config.BITPAPA_TOKEN)
        trades = await client.list_latest_trades()
        bots = [TradeBot(bitpapa_client=client, trade_id=trade.id) for trade in trades]
        await asyncio.gather(*[bot.process() for bot in bots])
