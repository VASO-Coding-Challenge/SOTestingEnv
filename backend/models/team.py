"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel, Relationship
import datetime

__authors__ = ["Nicholas Almy", "Andrew Lockard"]


class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    password: str
    start_time: datetime.time
    end_time: datetime.time
    login_time: datetime.timedelta | None
    members: list["TeamMember"] = Relationship(back_populates="team")
