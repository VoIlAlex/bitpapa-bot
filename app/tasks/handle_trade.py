import asyncio
from typing import List

from config import config
from db.models.trades import TradeRemoteStatus
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import Trade
from service.external.qiwi.client import QiwiClient
from service.trade_bot.bot import TradeBot
from tasks.base import Task


class TaskHandleTrade(Task):
    @staticmethod
    def filter_trades(trades: List[Trade]):
        new_trades = []
        for trade in trades:
            if trade.status not in [
                TradeRemoteStatus.CANCELLED.value,
                TradeRemoteStatus.CANCELLED_BY_ADMIN.value,
                TradeRemoteStatus.CANCELLED_BY_BUYER.value,
                TradeRemoteStatus.COMPLETED,
                TradeRemoteStatus.COMPLETED_BY_ADMIN,
                TradeRemoteStatus.COMPLETED_BY_SELLER
            ]:
                new_trades.append(trade)
        return new_trades

    @staticmethod
    async def execute():
        client = BitPapaClient(config.BITPAPA_TOKEN)
        trades = await client.list_latest_trades()
        trades = TaskHandleTrade.filter_trades(trades)
        qiwi_client = QiwiClient(token=config.QIWI_TOKEN)
        bots = [TradeBot(
            bitpapa_client=client,
            qiwi_client=qiwi_client,
            trade_id=trade.id,
            offer_id=trade.ad.id
        ) for trade in trades]
        await asyncio.gather(*[bot.process() for bot in bots])
