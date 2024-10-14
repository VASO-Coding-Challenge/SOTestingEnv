"""Model to crate a many to one relationship with the Team model"""
from sqlmodel import Field, SQLModel, Relationship
from .team import Team

__authors__ = ["Andrew Lockard"]

class TeamMember(SQLModel, table=True):
    """Stores one team member for a given team"""
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="members")