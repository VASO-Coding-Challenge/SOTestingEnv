"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard"]


class TeamBase(SQLModel):
    """Base model for Team table, this model should not be exported"""

    name: str
    start_time: datetime
    end_time: datetime


class Team(TeamBase, table=True):
    """Table Model for a Team Member"""

    id: int | None = Field(default=None, primary_key=True)
    password: str
    members: list["TeamMember"] = Relationship(
        cascade_delete=True, back_populates="team"
    )


class TeamData(TeamBase):
    """Model to define the creation shape of the team model"""

    password: str


class TeamPublic(TeamBase):
    """Model to define the API response shape of the Team model"""

    id: int
