"""Model for the Team table that stores official team information"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .session_obj import Session_Obj

__authors__ = [
    "Nicholas Almy",
    "Mustafa Aljumayli",
    "Andrew Lockard",
    "Ivan Wu",
    "Michelle Nguyen",
]


class TeamBase(SQLModel):
    """Base model for Team table, this model should not be exported"""

    name: str
    session_id: Optional[int] = Field(foreign_key="session_obj.id", nullable=True)


class Team(TeamBase, table=True):
    """Table Model for a Team"""

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    members: list["TeamMember"] = Relationship(back_populates="team")
    session: Optional["Session_Obj"] = Relationship(back_populates="teams")


class TeamData(TeamBase):
    """Model to define the creation shape of the team model"""
    
    password: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class TeamPublic(TeamBase):
    """Model to define the API response shape of the Team model"""

    id: int
    session: Optional["Session_Obj"]
