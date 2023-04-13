import asyncio

import pytest_asyncio
import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import create_database, database_exists, drop_database
from config import config
from db.models import *
from db.base import Base
from main import app
from httpx import AsyncClient


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def database(request):
    if database_exists(config.POSTGRES_URL_SYNC_TEST):
        drop_database(config.POSTGRES_URL_SYNC_TEST)

    create_database(config.POSTGRES_URL_SYNC_TEST)
    engine_to_create = create_engine(config.POSTGRES_URL_SYNC_TEST)
    Base.metadata.create_all(engine_to_create)

    @request.addfinalizer
    def drop_databases():
        drop_database(config.POSTGRES_URL_SYNC_TEST)
