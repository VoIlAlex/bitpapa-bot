import asyncio
from logging import getLogger
from typing import List

from config import config
from db.models import Trade
from db.models.trades import TradeRemoteStatus
from service.external.bitpapa.client import BitPapaClient
from service.external.bitpapa.schema import Trade as TradeData, OfferType
from tasks.base import Task


logger = getLogger(__name__)


class TaskFetchNewTrades(Task):
    @staticmethod
    def filter_trades(trades: List[TradeData]):
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
        trades = TaskFetchNewTrades.filter_trades(trades)
        logger.info(f"Trades after filtering: {len(trades)}")
        await Trade.bulk_create_if_not_exist([
            Trade(
                external_id=trade_data.id,
                external_ad_id=trade_data.ad.id,
                external_conversation_id=trade_data.conversation_id,
                contractor_id=trade_data.contractor.id,
                contractor_user_name=trade_data.contractor.user_name,
                amount=trade_data.amount,
                price=trade_data.price,
                cost=trade_data.cost,
                external_status=trade_data.status,
                external_created_at=trade_data.created_at,
                external_completed_at=trade_data.completed_at,
                external_cancelled_at=trade_data.cancelled_at,
                external_paid_confirmed_at=trade_data.paid_confirmed_at,
                external_escrow_expired_at=trade_data.escrow_expired_at,
                transaction_url=trade_data.transaction.url,
                transaction_txid=trade_data.transaction.txid,
                is_first=trade_data.is_first
            ) for trade_data in trades
        ])
