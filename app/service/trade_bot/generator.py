from datetime import datetime, timezone, timedelta
from uuid import uuid4

from config import config
from db.models import Trade, TradeMessage, Offer, TradeQiwiBill
from service.external.bitpapa.client import BitPapaClient
from service.external.qiwi.client import QiwiClient


class TradeBotGenerator:
    def __init__(
        self,
        bitpapa_client: BitPapaClient,
        trade_id: str,
        qiwi_client: QiwiClient
    ):
        self.bitpapa_client = bitpapa_client
        self.trade_id = trade_id
        self.qiwi_client = qiwi_client

    @staticmethod
    def generate_bill_id() -> str:
        return str(uuid4())

    async def generate_bill(
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
            customer_phone=trade.contractor_phone,
            customer_email=None,
            customer_account=None,
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
        return bill
