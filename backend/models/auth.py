from datetime import datetime
from sqlmodel import SQLModel, Field

from backend.models.team import Team

__authors__ = ["Mustafa Aljumayli"]


class Token(SQLModel, table=False):
    "Response Model for the token."
    access_token: str
    token_type: str


class TokenData(SQLModel, table=False):
    """This model represents the data encoded into a token."""

    id: int
    name: str
    exp: datetime


class LoginData(SQLModel, table=False):
    """This model represents the login data sent in the request for a token."""

    name: str
    password: str
    is_team: bool = Field(default=True)
