from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class SearchOfferUser(BaseModel):
    id: int
    user_name: str
    online: bool
    last_sign_in_at: datetime

    # TODO: should be handle those parameters
    is_guest: bool
    is_suspicious: bool
    is_verified: bool


class SearchOffer(BaseModel):
    id: str
    human_id: str
    crypto_currency_code: str
    type: str
    currency_code: str
    payment_method_code: str
    amount_min: float
    amount_max: float
    limit_min: float
    limit_max: float
    is_active: bool
    price: Decimal()
    user: SearchOfferUser


class SearchOffersResult(BaseModel):
    page: int
    pages: int
    total: int
    ads: List[SearchOffer]
