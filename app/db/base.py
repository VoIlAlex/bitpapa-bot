import sys

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession as _AsyncSession
from config import config

if 'pytest' in sys.modules:
    SQLALCHEMY_DATABASE_URL = config.POSTGRES_URL_TEST
else:
    SQLALCHEMY_DATABASE_URL = config.POSTGRES_URL


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSession = sessionmaker(bind=engine, class_=_AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with AsyncSession() as session:
        return session
