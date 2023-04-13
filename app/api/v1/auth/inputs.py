from pydantic import BaseModel


class RegisterInput(BaseModel):
    username: str
    password: str


class LoginInput(BaseModel):
    username: str
    password: str


class RefreshTokenInput(BaseModel):
    access_token: str
    refresh_token: str
