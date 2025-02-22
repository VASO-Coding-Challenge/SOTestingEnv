"""Model for the Team table that stores official team information"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:  # delayed import to avoid circular dependency
    from backend.models.session_obj import Session_Obj
    from backend.models.team_members import TeamMember

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard", "Ivan Wu"]


class TeamBase(SQLModel):
    """Base model for Team table, this model should not be exported"""

    name: str
    session_id: Optional[int] = Field(default=None, foreign_key="session_obj.id")


class Team(TeamBase, table=True):
    """Table Model for a Team"""

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str

    # Relationship with TeamMember (One-to-Many)
    members: list["TeamMember"] = Relationship(back_populates="team")

    # Relationship with Session_Obj (Many-to-One)
    session: Optional["Session_Obj"] = Relationship(back_populates="teams")


class TeamData(TeamBase):
    """Model to define the creation shape of the team model"""

    password: str


class TeamPublic(TeamBase):
    """Model to define the API response shape of the Team model"""

    id: int
    session: Optional["Session_Obj"]  # API response should include session details
