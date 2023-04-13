from datetime import datetime

from pydantic import BaseModel


class RegisterOutput(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime


class MeOutput(BaseModel):
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
