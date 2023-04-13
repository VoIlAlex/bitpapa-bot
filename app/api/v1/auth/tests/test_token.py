from httpx import AsyncClient

from db.models import User


async def test_api_auth_token_200(client: AsyncClient, user: User):
    response = await client.post(
        url="/api/users/v1/auth/token/",
        json={
            "username": user.username,
            "password": "test-password"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
