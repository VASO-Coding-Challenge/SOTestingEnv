"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

__authors__ = ["Ivan Wu"]


class Session(SQLModel):
    """Model for Sessions"""

    id: int | None = Field(default=None, primary_key=True)
    start_time: datetime
    end_time: datetime
