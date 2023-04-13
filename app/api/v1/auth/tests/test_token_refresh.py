from httpx import AsyncClient

from db.models import User
from service.auth.login import JWTService


async def test_api_auth_token_refresh_200(client: AsyncClient, user: User):
    access_token = JWTService.create_access_token(user)
    refresh_token = JWTService.create_refresh_token(user)

    response = await client.post(
        url="/api/users/v1/auth/token/refresh/",
        json={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
