from datetime import datetime, timezone, timedelta
from uuid import uuid4

from config import config
from db.models import Trade, TradeMessage, Offer, TradeQiwiBill
from service.external.bitpapa.client import BitPapaClient
from service.external.qiwi.client import QiwiClient


class TradeBotSyncer:
    def __init__(
        self,
        bitpapa_client: BitPapaClient,
        trade_id: str,
        qiwi_client: QiwiClient
    ):
        self.bitpapa_client = bitpapa_client
        self.trade_id = trade_id
        self.qiwi_client = qiwi_client

    async def sync_trade(self) -> Trade:
        trade_data = await self.bitpapa_client.get_trade(self.trade_id)
        trade = await Trade.get_by_external_id(self.trade_id)

        data_to_save = {
            "external_id": trade_data.id,
            "external_ad_id": trade_data.ad.id,
            "external_conversation_id": trade_data.conversation_id,
            "contractor_id": trade_data.contractor.id,
            "contractor_user_name": trade_data.contractor.user_name,
            "amount": trade_data.amount,
            "price": trade_data.price,
            "cost": trade_data.cost,
            "external_status": trade_data.status,
            "external_created_at": trade_data.created_at,
            "external_completed_at": trade_data.completed_at,
            "external_cancelled_at": trade_data.cancelled_at,
            "external_paid_confirmed_at": trade_data.paid_confirmed_at,
            "external_escrow_expired_at": trade_data.escrow_expired_at,
            "transaction_url": trade_data.transaction.url,
            "transaction_txid": trade_data.transaction.txid,
            "is_first": trade_data.is_first
        }

        if not trade:
            trade = await Trade.create(**data_to_save)
        else:
            await trade.update(**data_to_save)
        return trade

    async def sync_messages(self, trade_internal_id: int, skip_user_id: str = None):
        messages_res = await self.bitpapa_client.get_trade_conversation(self.trade_id)
        messages_data = [m for m in messages_res.messages if m.user_id != skip_user_id]
        messages = await TradeMessage.create_or_update_bulk(
            [{
                "external_id": message_data.id,
                "external_user_id": message_data.user_id,
                "body": message_data.body,
                "date": message_data.date,
                "attachment_url": message_data.attachment.url if message_data.attachment else None,
                "attachment_content_type": message_data.attachment.content_type if message_data.attachment else None,
                "trade_id": trade_internal_id,
            } for message_data in messages_data]
        )
        return messages

    async def sync_trade_bill(self, trade: Trade) -> TradeQiwiBill:
        bill = await TradeQiwiBill.get_by_trade_id(trade.id)
        bill_data = await self.qiwi_client.get_bill(bill_id=bill.bill_id)

        await bill.update(
            site_id=bill_data.siteId,
            bill_id=bill_data.billId,
            amount_value=bill_data.amount.value,
            amount_currency=bill_data.amount.currency,
            status_value=bill_data.status.value,
            status_changed_date_time=bill_data.status.changedDateTime,
            customer_email=bill_data.customer.email,
            customer_phone=bill_data.customer.phone,
            customer_account=bill_data.customer.account,
            comment=bill_data.comment,
            creation_date_time=bill_data.creationDateTime,
            expiration_date_time=bill_data.expirationDateTime,
            pay_url=bill_data.payUrl
        )

        return bill
