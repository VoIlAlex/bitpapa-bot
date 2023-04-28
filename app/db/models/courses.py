from typing import Optional, List, Union
from decimal import Decimal
from sqlalchemy import Column, Integer, String, DateTime, select, DECIMAL, Boolean, Text, true, BigInteger
from sqlalchemy.sql import func
from db.base import Base, AsyncSession


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer(), autoincrement=True, primary_key=True, index=True)

    price = Column(DECIMAL(12, 2), nullable=False)

    currency_code = Column(String(255))
    crypto_currency_code = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def get(currency_code: str, crypto_currency_code: str) -> Optional["Course"]:
        async with AsyncSession() as session:
            query = select(Course).where(
                Course.currency_code == currency_code,
                Course.crypto_currency_code == crypto_currency_code
            )
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def create(**kwargs):
        async with AsyncSession() as session:
            course = Course(**kwargs)
            session.add(course)
            await session.commit()
            await session.refresh(course)
        return course

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

    @staticmethod
    async def update_data(
        currency_code: str,
        crypto_currency_code: str,
        price: Union[Decimal, float, str]
    ) -> "Course":
        async with AsyncSession() as session:
            query = select(Course).where(
                Course.currency_code == currency_code,
                Course.crypto_currency_code == crypto_currency_code
            )
            result = await session.execute(query)
            course = result.scalar()

            if course is None:
                course = Course(
                    currency_code=currency_code,
                    crypto_currency_code=crypto_currency_code,
                    price=price
                )
                session.add(course)
                await session.commit()
                await session.refresh(course)

            elif course.price != price:
                course.price = price
                session.add(course)
                await session.commit()
                await session.refresh(course)

            return course
