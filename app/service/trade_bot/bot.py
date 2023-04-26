from datetime import datetime, timezone, timedelta
from logging import getLogger
from uuid import uuid4

from config import config
from db.models import Offer
from db.models.trades import Trade, TradeMessage, TradeQiwiBill, TradeStatus, TradeRemoteStatus
from service.external.bitpapa.client import BitPapaClient
from service.external.qiwi.client import QiwiClient
from service.templates_handlers import get_greeting_text, get_bill_text, get_cancel_text, get_paid_text

logger = getLogger(__name__)


class TradeBot:
    def __init__(
        self,
        bitpapa_client: BitPapaClient,
        qiwi_client: QiwiClient,
        trade_id: str,
        offer_id: str
    ):
        self.bitpapa_client = bitpapa_client
        self.qiwi_client = qiwi_client
        self.trade_id = trade_id
        self.offer_id = offer_id

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
            await Trade.create(**data_to_save)
        else:
            await trade.update(**data_to_save)
        return trade

    async def sync_messages(self, trade_internal_id: int):
        messages_res = await self.bitpapa_client.get_trade_conversation(self.trade_id)
        messages = await TradeMessage.create_or_update_bulk(
            [{
                "external_id": message_data.id,
                "external_user_id": message_data.user.id,
                "external_user_name": message_data.user.user_name,
                "body": message_data.body,
                "date": message_data.date,
                "attachment_url": message_data.attachment.url,
                "attachment_content_type": message_data.attachment.content_type,
                "trade_id": trade_internal_id,
            } for message_data in messages_res.messages]
        )
        return messages

    async def handle_message(
        self,
        offer: Offer,
        trade: Trade,
        message: TradeMessage
    ):
        # Place to put message handling
        await message.mark_as_handled()

    async def send_greeting(self):
        text = get_greeting_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=text
        )

    @staticmethod
    def generate_bill_id() -> str:
        return str(uuid4())

    async def generate_and_send_bill(
        self,
        offer: Offer,
        trade: Trade
    ) -> TradeQiwiBill:
        comment = f'Buy {trade.amount} {offer.crypto_currency_code} on Bitpapa.com.'
        expiration_date_time = datetime.now(tz=timezone.utc) + timedelta(seconds=config.QIWI_BILL_EXPIRATION_DELTA)
        bill_id = self.generate_bill_id()
        bill_data = await self.qiwi_client.create_bill(
            site_id=config.QIWI_SITE_ID,
            bill_id=bill_id,
            amount_value=trade.cost,
            amount_currency=offer.currency_code,
            comment=comment,
            expiration_date_time=expiration_date_time,
            customer_phone=...,
            customer_email=...,
            customer_account=...,
            custom_fields={
                "offer_id": trade.external_ad_id,
                "trade_id": trade.external_id,
            }
        )
        bill = await TradeQiwiBill.create(
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
            pay_url=bill_data.payUrl,
            trade_id=trade.id
        )
        bill_text = get_bill_text(bill_data.payUrl)
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=bill_text
        )
        return bill

    async def send_cancel_message(self):
        cancel_message = get_cancel_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=cancel_message
        )

    async def send_paid_message(self):
        paid_message = get_paid_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=paid_message
        )

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

    async def process(self):
        offer = await Offer.get_by_external_id(self.offer_id)

        if offer is None:
            logger.error(f"Offer \"{self.offer_id}\" does not exists. Create it to use.")
            return

        if not offer.is_initialized:
            logger.error(f"Offer \"{self.offer_id}\" is not initialized. Correct it to use.")
            return

        if not offer.is_active:
            logger.error(f"Offer \"{self.offer_id}\" is not active. Activate it to use.")
            return

        trade = await self.sync_trade()
        if trade.status in [
            TradeStatus.CANCELED.value,
            TradeStatus.COMPLETED.value,
            TradeStatus.PAID.value
        ]:
            return

        if trade.external_status and trade.external_status in [
            TradeRemoteStatus.CANCELLED.value,
            TradeRemoteStatus.CANCELLED_BY_ADMIN.value,
            TradeRemoteStatus.CANCELLED_BY_BUYER.value
        ]:
            await trade.update(
                status=TradeStatus.CANCELED.value
            )
            return

        if not trade.greeting_sent:
            await self.send_greeting()
            await trade.update(greeting_sent=True)

        if not offer.greeting_only:
            if trade.requisites_sent:
                bill = await self.sync_trade_bill(trade=trade)
                if bill.status_value == "PAID":
                    if offer.auto_trade_close:
                        await self.bitpapa_client.complete_trade(self.trade_id)
                        await trade.update(
                            status=TradeStatus.COMPLETED.value
                        )
                    else:
                        await self.send_paid_message()
                        await trade.update(
                            status=TradeStatus.PAID.value
                        )
                if bill.status_value in ["REJECTED", "EXPIRED"]:
                    await self.send_cancel_message()
                    await self.bitpapa_client.cancel_trade(self.trade_id)
                    await trade.update(
                        status=TradeStatus.CANCELED
                    )
            else:
                await self.generate_and_send_bill(
                    offer=offer,
                    trade=trade
                )
                await trade.update(requisites_sent=True)

            messages = await self.sync_messages(trade.id)
            unhandled_messages = sorted(
                [m for m in messages if not m.is_handled],
                key=lambda message: message.date
            )

            for message in unhandled_messages:
                await self.handle_message(
                    offer=offer,
                    trade=trade,
                    message=message
                )
