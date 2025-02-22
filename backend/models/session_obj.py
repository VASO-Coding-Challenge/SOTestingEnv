"""Model for the Session_Obj table that stores official Session_Obj information"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .team import Team  # delay the import to avoid circular issues

__authors__ = ["Ivan Wu", "Michelle Nguyen", "Tsering Lama"]


class Session_Obj(SQLModel, table=True):
    """Model for Sessions"""

    id: int = Field(default=None, primary_key=True)
    name: str
    start_time: datetime
    end_time: datetime

    # One-to-Many relationship with teams
    teams: List["Team"] = Relationship(back_populates="session")
