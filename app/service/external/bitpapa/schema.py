from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel


class SearchOfferUser(BaseModel):
    id: str
    user_name: str
    online: bool
    last_sign_in_at: datetime

    # TODO: should be handle those parameters
    is_guest: bool
    is_suspicious: bool
    # is_verified: bool


class SearchOffer(BaseModel):
    id: str
    crypto_currency_code: str
    type: str
    currency_code: str
    payment_method_code: str
    amount_min: float
    amount_max: float
    limit_min: float
    limit_max: float
    is_active: bool
    price: float
    user: SearchOfferUser
    human_id: Optional[str] = None


class SearchOffersResult(BaseModel):
    page: int
    pages: int
    total: int
    ads: List[SearchOffer]


class TradeConversationMessageUser(BaseModel):
    id: str
    user_name: str
    online: bool
    last_sign_in_at: datetime


class TradeConversationMessageAttachment(BaseModel):
    url: str
    content_type: str


class TradeConversationMessage(BaseModel):
    id: str
    user: TradeConversationMessageUser
    body: str
    date: datetime
    attachment: Optional[TradeConversationMessageAttachment]
    is_read: bool
    external_id: str


class TradeConversation(BaseModel):
    messages: List[TradeConversationMessage]


class TradeAd(BaseModel):
    id: str
    type: str


class TradeContractor(BaseModel):
    id: str
    user_name: str


class TradeTransaction(BaseModel):
    url: str
    txid: str


class Trade(BaseModel):
    id: str
    ad: TradeAd
    contractor: TradeContractor
    amount: float
    status: str
    price: float
    cost: float
    created_at: datetime
    conversation_id: str
    completed_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    paid_confirmed_at: Optional[datetime]
    escrow_expired_at: Optional[datetime]
    transaction: TradeTransaction
    current_time: str
    is_first: bool


class ExchangeRate(BaseModel):
    currency_code: str
    crypto_currency_code: str
    price: float
