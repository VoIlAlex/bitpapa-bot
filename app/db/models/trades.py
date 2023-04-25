import enum
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, String, DateTime, select, DECIMAL, Boolean, Text, true, BigInteger, ForeignKey
from sqlalchemy.sql import func
from db.base import Base, AsyncSession


class TradeRemoteStatus(enum.Enum):
    NEW = "new"
    DISPUT = "disput"
    PAID_CONFIRMED = "paid_confirmed"
    COMPLETED_BY_SELLER = "completed_by_seller"
    COMPLETED_BY_ADMIN = "completed_by_admin"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    CANCELLED_BY_ADMIN = "cancelled_by_admin"
    CANCELLED_BY_BUYER = "cancelled_by_buyer"
    EXPIRED_AND_PAID = "expired_and_paid"
    EXPIRED = "expired"


class TradeStatus(enum.Enum):
    NEW = "new"
    HELLO_MESSAGE_SENT = "hello"


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer(), autoincrement=True, primary_key=True, index=True)

    external_id = Column(String(255), unique=True)
    external_ad_id = Column(String(255))
    external_conversation_id = Column(String(255))

    contractor_id = Column(String(255))
    contractor_user_name = Column(String(255))

    amount = Column(DECIMAL(12, 2))
    status = Column(String(127))
    price = Column(DECIMAL(12, 2))
    cost = Column(DECIMAL(12, 2))

    external_created_at = Column(DateTime(timezone=True))
    external_completed_at = Column(DateTime(timezone=True), nullable=True)
    external_cancelled_at = Column(DateTime(timezone=True), nullable=True)
    external_paid_confirmed_at = Column(DateTime(timezone=True), nullable=True)
    external_escrow_expired_at = Column(DateTime(timezone=True), nullable=True)

    transaction_url = Column(String(512), nullable=True)
    transaction_txid = Column(String(512), nullable=True)

    is_first = Column(Boolean(), default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_by_external_id(trade_id: str) -> Optional["Trade"]:
        async with AsyncSession() as session:
            query = select(Trade).where(Trade.external_id == trade_id)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def get_by_id(id_: int) -> Optional["Trade"]:
        async with AsyncSession() as session:
            query = select(Trade).where(Trade.id == id_)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def create(
        external_id: str,
        external_ad_id: str,
        external_conversation_id: str,
        contractor_id: str,
        contractor_user_name: str,
        amount: float,
        status: str,
        price: float,
        cost: float,
        external_created_at: datetime,
        external_completed_at: datetime,
        external_cancelled_at: datetime,
        external_paid_confirmed_at: datetime,
        external_escrow_expired_at: datetime,
        transaction_url: str,
        transaction_txid: str,
        is_first: bool,
    ):
        async with AsyncSession() as session:
            trade = Trade(
                external_id=external_id,
                external_ad_id=external_ad_id,
                external_conversation_id=external_conversation_id,
                contractor_id=contractor_id,
                contractor_user_name=contractor_user_name,
                amount=amount,
                status=status,
                price=price,
                cost=cost,
                external_created_at=external_created_at,
                external_completed_at=external_completed_at,
                external_cancelled_at=external_cancelled_at,
                external_paid_confirmed_at=external_paid_confirmed_at,
                external_escrow_expired_at=external_escrow_expired_at,
                transaction_url=transaction_url,
                transaction_txid=transaction_txid,
                is_first=is_first,
            )
            session.add(trade)
            await session.commit()
            await session.refresh(trade)
        return trade

    async def update(self, **kwargs):
        async with AsyncSession() as session:
            for key, value in kwargs.items():
                setattr(self, key, value)
            session.add(self)
            await session.commit()
            await session.refresh(self)


class TradeMessage(Base):
    __tablename__ = "trades_messages"

    id = Column(Integer(), autoincrement=True, primary_key=True, index=True)
    external_id = Column(String(255), unique=True)
    external_user_id = Column(String(255))
    external_user_name = Column(String(255))

    body = Column(Text())
    date = Column(DateTime(timezone=True))

    attachment_url = Column(String(512), nullable=True)
    attachment_content_type = Column(String(127), nullable=True)

    is_handled = Column(Boolean(), nullable=False, default=False)

    trade_id = Column(ForeignKey("trades.id"))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def create_or_update_bulk(data: List[dict]):
        objs = []

        async with AsyncSession() as session:
            for data_item in data:
                query = select(TradeMessage).where(TradeMessage.external_id == data_item["external_id"])
                result = session.execute(query)
                message = result.scalar()

                if message:
                    for key, value in data_item.items():
                        setattr(message, key, value)
                    session.add(message)
                else:
                    message = TradeMessage({
                        **data_item
                    })
                    session.add(message)

                await session.flush()

                objs.append(message)
            await session.commit()
            for obj in objs:
                await session.refresh(obj)
        return objs

    async def mark_as_handled(self):
        async with AsyncSession() as session:
            self.is_handled = True
            session.add(self)
            await session.commit()
            await session.refresh(self)
