from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OfferOutput(BaseModel):
    id: int

    number: str
    min_price: float
    beat_price_by: float

    greeting_only: bool
    auto_trade_close: bool

    search_price_limit_min: float
    search_price_limit_max: float
    search_minutes_offline_max: float

    current_price: Optional[float]
    current_price_last_updated: Optional[datetime]
    current_price_last_response_duration: Optional[int]

    current_min_price: Optional[float]
    current_min_price_last_updated: Optional[datetime]
    current_min_price_last_response_duration: Optional[int]
    current_min_price_total_duration: Optional[int]
    current_min_price_requests_number: Optional[int]
    current_min_price_found: Optional[bool]

    is_initialized: bool
    init_error: Optional[str]
    is_active: bool

    currency_code: Optional[str]
    crypto_currency_code: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
