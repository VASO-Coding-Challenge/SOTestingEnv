"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel
import datetime

__authors__ = ["Nicholas Almy"]


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(example="c2")
    password: str = Field(example="pie-cake-banana")
    login_time: datetime.timedelta
