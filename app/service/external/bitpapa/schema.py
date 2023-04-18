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
