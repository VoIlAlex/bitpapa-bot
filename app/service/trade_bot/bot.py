import re
from datetime import datetime, timezone, timedelta
from logging import getLogger
from types import SimpleNamespace
from uuid import uuid4

from config import config
from db.models import Offer
from db.models.trades import Trade, TradeMessage, TradeQiwiBill, TradeStatus, TradeRemoteStatus
from service.external.bitpapa.client import BitPapaClient
from service.external.qiwi.client import QiwiClient
from service.templates_handlers import get_greeting_text, get_bill_text, get_paid_text, \
    get_wrong_phone_format_text, get_phone_success_text
from service.trade_bot.generator import TradeBotGenerator
from service.trade_bot.messenger import TradeBotMessenger
from service.trade_bot.syncer import TradeBotSyncer
from service.trade_bot.validation import validate_phone

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
        self.messenger = TradeBotMessenger(
            trade_id=trade_id,
            bitpapa_client=bitpapa_client
        )
        self.syncer = TradeBotSyncer(
            trade_id=trade_id,
            bitpapa_client=bitpapa_client,
            qiwi_client=qiwi_client
        )
        self.generator = TradeBotGenerator(
            trade_id=trade_id,
            bitpapa_client=bitpapa_client,
            qiwi_client=qiwi_client
        )

    async def handle_message(
        self,
        offer: Offer,
        trade: Trade,
        message: TradeMessage
    ):
        if trade.contractor_phone is None:
            try:
                phone = validate_phone(message.body)
                await trade.update(
                    contractor_phone=phone
                )
                await self.messenger.send_phone_retrieve_success()
            except RuntimeError:
                await self.messenger.send_wrong_phone_format()
        await message.mark_as_handled()

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

        trade = await self.syncer.sync_trade()
        if trade.status in [
            TradeStatus.CANCELED.value,
            TradeStatus.COMPLETED.value,
            TradeStatus.PAID.value
        ]:
            return

        if trade.external_status and trade.external_status in [
            TradeRemoteStatus.CANCELLED.value,
            TradeRemoteStatus.CANCELLED_BY_ADMIN.value,
            TradeRemoteStatus.CANCELLED_BY_BUYER.value,
        ] or trade.external_cancelled_at is not None:
            await trade.update(
                status=TradeStatus.CANCELED.value
            )
            return

        if trade.external_status and trade.external_status in [
            TradeRemoteStatus.COMPLETED.value,
            TradeRemoteStatus.COMPLETED_BY_SELLER.value,
            TradeRemoteStatus.COMPLETED_BY_ADMIN.value,
        ] or trade.external_completed_at is not None:
            await trade.update(
                status=TradeStatus.COMPLETED.value
            )
            return

        if not trade.greeting_sent:
            await self.messenger.send_greeting()
            await trade.update(greeting_sent=True)

        if not offer.greeting_only and trade.contractor_phone:
            if trade.requisites_sent:
                if trade.external_status == TradeRemoteStatus.PAID_CONFIRMED.value:
                    # TODO: remove mock
                    bill = SimpleNamespace(
                        status_value="PAID"
                    )
                    # bill = await self.syncer.sync_trade_bill(trade=trade)
                    if bill.status_value == "PAID":
                        await self.messenger.send_paid_message()
                        if offer.auto_trade_close:
                            await self.bitpapa_client.complete_trade(self.trade_id)
                            await trade.update(
                                status=TradeStatus.COMPLETED.value
                            )
                        else:
                            await trade.update(
                                status=TradeStatus.PAID.value
                            )
                    else:
                        if trade.status != TradeStatus.PAYMENT_NOT_RECEIVED.value:
                            await self.messenger.send_payment_failed()
                            # await self.bitpapa_client.cancel_trade(self.trade_id)
                            await trade.update(
                                status=TradeStatus.PAYMENT_NOT_RECEIVED.value
                            )
            else:
                # TODO: remove mock
                bill = SimpleNamespace(
                    pay_url="http://example.com/"
                )
                # bill = await self.generator.generate_bill(offer=offer, trade=trade)
                await self.messenger.send_bill(bill.pay_url)
                await trade.update(requisites_sent=True)

        messages = await self.syncer.sync_messages(trade.id, skip_user_id=offer.user_id)
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
