"""Model for the Team table that stores words for password generation"""

from sqlmodel import Field, SQLModel
from datetime import datetime

__authors__ = ["Nicholas Almy"]


class Word(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    word: str
    used: bool = Field(default=False)
