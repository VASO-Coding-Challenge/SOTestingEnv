"""Model for the Session_Obj table that stores official Session_Obj information"""


from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from models.team import Team  # import team model for association table

__authors__ = ["Ivan Wu", "Michelle Nguyen", "Tsering Lama"]


class Session_Obj(SQLModel, table=True):
    """Model for Sessions"""

    id: int = Field(default=None, primary_key=True)
    name: str
    start_time: datetime
    end_time: datetime

    # One-to-Many relationship with teams
    teams: List["Team"] = Relationship(back_populates="session")


class Team(TeamBase, table=True):
    """Table Model for a Team"""

    id: int = Field(default=None, primary_key=True)
    password: str

    # foreign Key linking a team to a session (each team has one session)
    session_id: Optional[int] = Field(default=None, foreign_key="session_obj.id")

    # relationship back to Session
    session: Optional["Session_Obj"] = Relationship(back_populates="teams")
