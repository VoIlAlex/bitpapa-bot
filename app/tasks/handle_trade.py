import asyncio
from logging import getLogger
from typing import List

from config import config
from db.models.trades import TradeRemoteStatus
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import Trade, OfferType
from service.external.qiwi.client import QiwiClient
from service.trade_bot.bot import TradeBot
from tasks.base import Task


logger = getLogger(__name__)


class TaskHandleTrade(Task):
    @staticmethod
    def filter_trades(trades: List[Trade]):
        new_trades = []
        for trade in trades:
            if trade.ad.type != OfferType.SELL.value:
                logger.info(f"Trade {trade.id} has wrong ad type. {trade.ad.type}")
                continue
            if trade.status in [
                TradeRemoteStatus.CANCELLED.value,
                TradeRemoteStatus.CANCELLED_BY_ADMIN.value,
                TradeRemoteStatus.CANCELLED_BY_BUYER.value,
                TradeRemoteStatus.COMPLETED,
                TradeRemoteStatus.COMPLETED_BY_ADMIN,
                TradeRemoteStatus.COMPLETED_BY_SELLER
            ]:
                logger.info(f"Trade {trade.id} is completed or canceled. {trade.status}")
                continue
            if trade.cancelled_at is not None:
                logger.info(f"Trade {trade.id} is already cancelled. {trade.cancelled_at}")
                continue
            if trade.completed_at is not None:
                logger.info(f"Trade {trade.id} is already completed. {trade.completed_at}")
                continue
            new_trades.append(trade)
        return new_trades

    @staticmethod
    async def execute():
        client = BitPapaClient(config.BITPAPA_TOKEN)
        trades = await client.list_latest_trades()
        logger.info(f"Trades before filtering: {len(trades)}")
        trades = TaskHandleTrade.filter_trades(trades)
        logger.info(f"Trades after filtering: {len(trades)}")
        qiwi_client = QiwiClient(token=config.QIWI_TOKEN)
        bots = [TradeBot(
            bitpapa_client=client,
            qiwi_client=qiwi_client,
            trade_id=trade.id,
            offer_id=trade.ad.id
        ) for trade in trades]
        await asyncio.gather(*[bot.process() for bot in bots])
