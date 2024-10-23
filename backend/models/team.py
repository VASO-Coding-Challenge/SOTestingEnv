"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel
import datetime

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli"]


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    start_time: datetime.time
    end_time: datetime.time
    active_JWT: bool = Field(default=False)
