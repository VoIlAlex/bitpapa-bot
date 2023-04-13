from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, select
from sqlalchemy.sql import func
from db.base import Base, AsyncSession


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), autoincrement=True, primary_key=True, index=True)
    username = Column(String(length=127), unique=True, nullable=False, index=True)
    password_hash = Column(String(length=512), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    @staticmethod
    async def get_by_username(username: str) -> Optional["User"]:
        async with AsyncSession() as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)
            return result.scalar()

    @staticmethod
    async def create(username: str, password_hash: str) -> "User":
        async with AsyncSession() as session:
            user = User(username=username, password_hash=password_hash)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user

    async def change_password(self, password_hash: str):
        async with AsyncSession() as session:
            self.password_hash = password_hash
            session.add(self)
            await session.commit()
            await session.refresh(self)

    @staticmethod
    async def get_by_id(id_: int) -> Optional["User"]:
        async with AsyncSession() as session:
            query = select(User).where(User.id == id_)
            result = await session.execute(query)
            return result.scalar()

