from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError, BaseModel

from config import config
from db.models.users import User
from service.auth.hash import HashService


class LoginService:
    @staticmethod
    async def login(username: str, password: str) -> Optional[User]:
        user = await User.get_by_username(username=username)
        if user is None:
            return None
        match = HashService.check_password(
            password=password,
            password_hash=user.password_hash
        )
        if not match:
            return None
        return user


class TokenPayload(BaseModel):
    exp: float
    sub: int


class JWTService:
    bearer_oauth = HTTPBearer(
        scheme_name="JWT"
    )

    @staticmethod
    def create_access_token(user: User) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(user.id)}
        encoded_jwt = jwt.encode(to_encode, config.JWT_SECRET_KEY, config.JWT_ALGORITHM)
        return encoded_jwt.decode("UTF-8")

    @staticmethod
    def create_refresh_token(user: User) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=config.JWT_REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(user.id)}
        encoded_jwt = jwt.encode(to_encode, config.JWT_REFRESH_SECRET_KEY, config.JWT_ALGORITHM)
        return encoded_jwt.decode("UTF-8")

    @staticmethod
    def get_token_payload(jwt_token: str, secret: str = config.JWT_SECRET_KEY) -> TokenPayload:
        try:
            payload = jwt.decode(
                jwt_token, secret, algorithms=[config.JWT_ALGORITHM]
            )
            token_payload = TokenPayload(**payload)
        except(jwt.exceptions.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_payload

    @staticmethod
    async def get_current_user(jwt_token: HTTPAuthorizationCredentials = Depends(bearer_oauth)) -> User:
        try:
            credentials = jwt_token.credentials
            token_payload = JWTService.get_token_payload(credentials)
            if datetime.fromtimestamp(token_payload.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except(jwt.exceptions.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user: User = await User.get_by_id(token_payload.sub)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        return user

    @staticmethod
    def check_for_refresh(access_token: str, refresh_token: str) -> int:
        try:
            access_token_payload = JWTService.get_token_payload(access_token)

            refresh_token_payload = JWTService.get_token_payload(
                refresh_token,
                secret=config.JWT_REFRESH_SECRET_KEY
            )
            if datetime.fromtimestamp(refresh_token_payload.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if access_token_payload.sub != refresh_token_payload.sub:
                raise ValidationError

            return access_token_payload.sub
        except(jwt.exceptions.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
