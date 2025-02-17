"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

__authors__ = ["Ivan Wu"]


class Session_Obj(SQLModel, table=True):
    """Model for Sessions"""

    id: int = Field(primary_key=True)
    name: str
    start_time: datetime
    end_time: datetime
