from pydantic import BaseModel


class OfferInput(BaseModel):
    number: str
    min_price: float
    beat_price_by: float

    greeting_only: bool
    auto_trade_close: bool

    search_price_limit_min: float
    search_price_limit_max: float
    search_minutes_offline_max: float
