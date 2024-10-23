from datetime import datetime
from sqlmodel import SQLModel, Field

from backend.models.team import Team

__authors__ = ["Mustafa Aljumayli"]


class Token(SQLModel, table=False):
    access_token: str
    token_type: str


class TokenData(SQLModel, table=False):
    id: int
    name: str
    expiration_time: str


class LoginData(SQLModel, table=False):
    name: str
    password: str
