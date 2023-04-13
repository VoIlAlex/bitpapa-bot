import pytest_asyncio

from service.auth.register import RegisterService


@pytest_asyncio.fixture(scope="session")
async def user(event_loop):
    user = await RegisterService.register_user(
        username="test-user",
        password="test-password",
        get_on_exists=True
    )
    return user
