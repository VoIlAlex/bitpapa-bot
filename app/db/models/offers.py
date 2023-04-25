from typing import Optional, List

from sqlalchemy import Column, Integer, String, DateTime, select, DECIMAL, Boolean, Text, true, BigInteger
from sqlalchemy.sql import func
from db.base import Base, AsyncSession


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer(), autoincrement=True, primary_key=True, index=True)

    number = Column(String(255), nullable=False, unique=True)
    min_price = Column(DECIMAL(12, 2), nullable=False)
    beat_price_by = Column(DECIMAL(12, 2), nullable=False)
    
    greeting_only = Column(Boolean(), nullable=False)
    auto_trade_close = Column(Boolean(), nullable=False)

    search_price_limit_min = Column(DECIMAL(12, 2), nullable=False)
    search_price_limit_max = Column(DECIMAL(12, 2), nullable=False)
    search_minutes_offline_max = Column(Integer(), nullable=False)

    is_initialized = Column(Boolean(), nullable=False, default=False)
    init_error = Column(Text(), nullable=True, default=None)
    is_active = Column(Boolean(), nullable=False, default=True)
    currency_code = Column(String(255))
    crypto_currency_code = Column(String(255))

    # Durations are in microseconds

    current_price = Column(DECIMAL(12, 2), nullable=True)
    current_price_last_updated = Column(DateTime(timezone=True), nullable=True)
    current_price_total_duration = Column(BigInteger(), nullable=True)
    current_price_last_request_time = Column(DateTime(timezone=True), nullable=True)
    current_price_last_request_block = Column(Integer(), nullable=True)

    current_min_price = Column(DECIMAL(12, 2), nullable=True)
    current_min_price_last_updated = Column(DateTime(timezone=True), nullable=True)
    current_min_price_last_response_duration = Column(BigInteger(), nullable=True)
    current_min_price_total_duration = Column(BigInteger(), nullable=True)
    current_min_price_requests_number = Column(Integer(), nullable=True)
    current_min_price_found = Column(Boolean(), default=False, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_by_id(id_: int) -> Optional["Offer"]:
        async with AsyncSession() as session:
            query = select(Offer).where(Offer.id == id_)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_by_external_id(offer_id: str) -> Optional["Offer"]:
        async with AsyncSession() as session:
            query = select(Offer).where(Offer.number == offer_id)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_all() -> List["Offer"]:
        async with AsyncSession() as session:
            query = select(Offer)
            result = await session.execute(query)
            return [x[0] for x in result.fetchall()]

    @staticmethod
    async def get_all_active() -> List["Offer"]:
        async with AsyncSession() as session:
            query = select(Offer).where(
                Offer.is_initialized == true(),
                Offer.is_active == true(),
            )
            result = await session.execute(query)
            return [x[0] for x in result.fetchall()]

    @staticmethod
    async def create(**kwargs):
        async with AsyncSession() as session:
            offer = Offer(**kwargs)
            session.add(offer)
            await session.commit()
            await session.refresh(offer)
        return offer

    async def update(self, **kwargs):
        async with AsyncSession() as session:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.add(self)
            await session.commit()
            await session.refresh(self)

    async def delete(self):
        async with AsyncSession() as session:
            session.add(self)
            await session.delete(self)
            await session.commit()
