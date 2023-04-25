from db.models import Offer
from db.models.trades import Trade, TradeMessage
from service.external.bitpapa.client import BitPapaClient


class TradeBot:
    def __init__(
        self,
        bitpapa_client: BitPapaClient,
        trade_id: str
    ):
        self.bitpapa_client = bitpapa_client
        self.trade_id = trade_id

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
            "status": trade_data.status,
            "price": trade_data.price,
            "cost": trade_data.cost,
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
        # TODO: implement message handling logic
        ...
        await message.mark_as_handled()

    async def process(self):
        trade = await self.sync_trade()
        messages = await self.sync_messages(trade.id)
        offer = await Offer.get_by_external_id(trade.external_ad_id)

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

