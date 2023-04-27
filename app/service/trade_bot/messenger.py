from service.external.bitpapa.client import BitPapaClient
from service.templates_handlers import get_phone_success_text, get_wrong_phone_format_text, get_greeting_text, \
    get_cancel_text, get_paid_text, get_bill_text


class TradeBotMessenger:
    def __init__(self, bitpapa_client: BitPapaClient, trade_id: str):
        self.bitpapa_client = bitpapa_client
        self.trade_id = trade_id

    async def send_phone_retrieve_success(self):
        text = get_phone_success_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=text
        )

    async def send_wrong_phone_format(self):
        text = get_wrong_phone_format_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=text
        )

    async def send_greeting(self):
        text = get_greeting_text()
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=text
        )

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

    async def send_bill(self, pay_url: str):
        text = get_bill_text(pay_url)
        await self.bitpapa_client.create_message_in_trade_conversation(
            trade_id=self.trade_id,
            body=text
        )
