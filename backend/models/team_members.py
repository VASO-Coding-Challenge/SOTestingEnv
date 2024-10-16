"""Models to crate a many to one relationship with the Team model.

Multiple models designed as per: https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/#use-multiple-models-to-create-a-hero
"""
from sqlmodel import Field, SQLModel, Relationship
from .team import Team

__authors__ = ["Andrew Lockard"]

class TeamMemberBase(SQLModel):
    """Base class to represent a TeamMember, this model should not be exported."""
    first_name: str
    last_name: str

class TeamMember(TeamMemberBase, table=True):
    """Table Model for a Team Member"""
    id: int | None = Field(default=None, primary_key=True)
    team_id: int = Field(foreign_key="team.id")
    team: Team = Relationship(back_populates="members")

class TeamMemberCreate(TeamMemberBase):
    """Model to define API creation shape, same shape as base, created just for convention"""
    pass

class TeamMemberPublic(TeamMemberBase):
    """Model to define API response shape"""
    id: int