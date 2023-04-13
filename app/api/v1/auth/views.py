from fastapi import HTTPException, status, Depends

from api.v1.auth.inputs import LoginInput, RefreshTokenInput
from api.v1.auth.outputs import MeOutput
from db.models import User
from service.auth.login import LoginService
from service.auth.login import JWTService


async def token_view(body: LoginInput):
    user = await LoginService.login(
        username=body.username,
        password=body.password
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Bad credentials.")
    access_token = JWTService.create_access_token(user)
    refresh_token = JWTService.create_refresh_token(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


async def refresh_view(body: RefreshTokenInput):
    user_id = JWTService.check_for_refresh(body.access_token, body.refresh_token)
    user = await User.get_by_id(user_id)
    access_token = JWTService.create_access_token(user)
    refresh_token = JWTService.create_refresh_token(user)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


async def me_view(user: User = Depends(JWTService.get_current_user)) -> MeOutput:
    return MeOutput(
        id=user.id,
        username=user.username,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
