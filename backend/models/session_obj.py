"""Model for the Session_Obj table that stores official Session_Obj information"""

from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

__authors__ = ["Ivan Wu", "Michelle Nguyen", "Tsering Lama"]


class SessionBase(SQLModel):
    """Base model for Sessions"""

    name: str
    start_time: datetime
    end_time: datetime
    # team_ids: Optional[List[int]] = None


class Session_Obj(SessionBase, table=True):
    """Database Model for Sessions"""

    id: int = Field(default=None, primary_key=True)
    teams: List["Team"] = Relationship(back_populates="session")


class SessionPublic(SessionBase):
    """Public API response model for a session"""

    id: int
    teams: List[int]
