"""Model for the Team table that stores official team information"""

from typing import Optional
from sqlmodel import Field, SQLModel, Relationship, Session

from backend.models.session_obj import Session_Obj
from backend.models.team_members import TeamMember

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard", "Ivan Wu"]


class TeamBase(SQLModel):
    """Base model for Team table, this model should not be exported"""

    name: str
    session_id: Optional[int] = Field(
        default=None, foreign_key="session.id", ondelete="CASCADE"
    )


class Team(TeamBase, table=True):
    """Table Model for a Team Member"""

    id: int | None = Field(default=None, primary_key=True)
    password: str
    members: list["TeamMember"] = Relationship(
        cascade_delete=True, back_populates="team"
    )
    session_id: Optional[int] = Field(default=None, foreign_key="session_obj.id")
    session: Optional["Session_Obj"] = Relationship(back_populates="teams")


class TeamData(TeamBase):
    """Model to define the creation shape of the team model"""

    password: str


class TeamPublic(TeamBase):
    """Model to define the API response shape of the Team model"""

    id: int
    session: Optional["Session_Obj"]  # necessary?
