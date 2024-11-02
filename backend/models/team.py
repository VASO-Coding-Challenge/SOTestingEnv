"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel
from datetime import datetime

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli"]


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    start_time: datetime
    end_time: datetime
    active_JWT: bool = Field(default=False)


class TeamData(SQLModel, table=False):
    name: str
    password: str
    start_time: datetime
    end_time: datetime
