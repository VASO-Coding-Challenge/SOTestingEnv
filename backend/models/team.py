"""Model for the Team table that stores official team information"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from .session_obj import Session_Obj

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard", "Ivan Wu"]


class TeamBase(SQLModel):
    """Base model for Team table, this model should not be exported"""

    name: str
    session_id: Optional[int] = Field(foreign_key="session_obj.id", ondelete="CASCADE")


class Team(TeamBase, table=True):
    """Table Model for a Team"""

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str

    # 1-to-m relationship with TeamMember
    members: list["TeamMember"] = Relationship(back_populates="team")

    # m-to-1 relationship with Session_Obj
    session: Optional["Session_Obj"] = Relationship(back_populates="teams")


class TeamData(TeamBase):
    """Model to define the creation shape of the team model"""

    password: str


class TeamPublic(TeamBase):
    """Model to define the API response shape of the Team model"""

    id: int
    session: Optional["Session_Obj"]
