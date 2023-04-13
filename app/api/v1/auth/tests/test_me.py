from httpx import AsyncClient

from db.models import User
from service.auth.login import JWTService


async def test_api_auth_me_200(client: AsyncClient, user: User):
    access_token = JWTService.create_access_token(user)

    response = await client.get(
        url="/api/users/v1/auth/me/",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["username"] == user.username
    assert data["created_at"] == user.created_at.isoformat()
    assert data["updated_at"] == user.updated_at.isoformat()
    assert "password" not in data
    assert "password_hash" not in data
