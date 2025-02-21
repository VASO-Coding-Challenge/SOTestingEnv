# """Model for the Team table that stores official team information"""

# from sqlmodel import Field, SQLModel, Relationship
# from datetime import datetime

# __authors__ = ["Ivan Wu"]


# class Session_Obj(SQLModel, table=True):
#     """Model for Sessions"""

#     id: int = Field(primary_key=True)
#     name: str
#     start_time: datetime
#     end_time: datetime

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from models.team import Team  # import team model for association table

__authors__ = ["Ivan Wu", "Michelle Nguyen", "Tsering Lama"]


# class Session_Obj(SQLModel, table=True):
#     """Model for Sessions"""

#     id: int = Field(default=None, primary_key=True)
#     name: str
#     start_time: datetime
#     end_time: datetime

#     # m-to-m relationship with teams
#     teams: List["Team"] = Relationship(
#         back_populates="sessions", link_model="SessionTeamLink"
#     )


# class SessionTeamLink(SQLModel, table=True):
#     """Association table between Sessions and Teams"""

#     session_id: int = Field(foreign_key="session_obj.id", primary_key=True)
#     team_id: int = Field(foreign_key="team.id", primary_key=True)


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
