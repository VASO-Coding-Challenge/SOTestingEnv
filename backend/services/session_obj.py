"""Service to handle the Session Objects feature"""

from typing import List
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select, and_, delete
import polars as pl
import datetime as dt

from .exceptions import (
    ResourceNotFoundException,
    InvalidCredentialsException,
    ResourceNotAllowedException,
)

from ..models.session_obj import Session_Obj
from ..services import team

__authors__ = ["Michelle Nguyen", "Tsering Lama"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class Session_ObjService:
    """Service that preforms actions on Session Objects."""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    # need to update what teams correspond with the session
    def update_session_obj(self, session_obj: Session_Obj) -> Session_Obj:
        """Update a session object in the database.
        Args:
            session (session_obj): session object to update
        Returns:
            Team: Updated session object
        Raises:
            ResourceNotFoundException: If the team does not exist in the database
        """
        existing_session: Session_Obj | None = self._session.exec(
            select(Team).where(Team.name == team.name)
        ).one_or_none()
        if Session_Obj:
            existing_session.name = session_obj.name
            existing_session.start_time = session_obj.start_time
            existing_session.end_time = session_obj.end_time
            self._session.add(existing_session)
            self._session.commit()
            return existing_session
        else:
            raise ResourceNotFoundException("Session", session_obj.name)

    def create_session_obj(self, session_obj: Session_Obj | TeamData) -> Session_Obj:
        """Create a new session object in the database.
        Args:
            session_obj (Session_Obj): Session object to create
        Returns:
            Team: Created Session_Obj object
        """
        if isinstance(team, TeamData):
            team = Team(
                name=team.name,
                password=team.password,
                start_time=team.start_time,
                end_time=team.end_time,
            )
        self._session.add(team)
        self._session.commit()
        return team

    def get_session_obj(self, identifier) -> Session_Obj:
        """Gets the session_obj by id (int) or name (str)"""
        # TODO: Improve documentation
        if isinstance(identifier, int):
            session_obj = self._session.get(Session_Obj, identifier)
            if team is None:
                raise ResourceNotFoundException(
                    f"Session_Obj with id={identifier} was not found"
                )
        elif isinstance(identifier, str):
            team = self._session.exec(
                select(Session_Obj).where(Session_Obj.name == identifier)
            ).first()
            if not session_obj:
                raise ResourceNotFoundException(
                    f"Session_Obj with name={identifier} was not found"
                )
        else:
            raise ValueError("Identifier must be an int (id) or a str (name)")
        return session_obj

    def get_all_session_objs(self) -> List[Session_Obj]:
        """Gets a list of all the sessions"""
        session_objs = self._session.exec(select(Session_Obj)).all()
        return session_objs

    def delete_all_session_objs(self):
        """Deletes all teams"""
        self._session.exec(delete(Session_Obj))
        # self._session.exec(delete(TeamMember)) # must remove all the teams associated with the session. set to null?
        self._session.commit()
        return True

    def delete_session_obj(self, session_obj: TeamData | Team) -> bool:
        """Deletes a team"""
        session_obj = self.get_session_obj(session_obj.name)
        self._session.delete(session_obj)
        self._session.commit()
        return True

    def add_team_member_session_obj(
        self, new_member: TeamMemberCreate, team: Team
    ) -> TeamMember:
        """Adds a new team member to team: team_id.
        Args:
            team: (Team): Team object of currently logged in user
            new_member (TeamMemberCreate): Data for new member
        Returns:
            TeamMember: The team member object that was added
        """
        member = TeamMember(
            team_id=team.id,
            first_name=new_member.first_name,
            last_name=new_member.last_name,
            id=None,
        )
        self._session.add(member)
        self._session.commit()
        self._session.refresh(member)
        return member

    def delete_team_member_session_obj(self, member_id: int, team: Team) -> None:
        """Deletes team member with member_id only if they are on team team_id.
        Args:
            member_id (int): team member to delete
            team: (Team): Team object of currently logged in user
        Raises:
            ResourceNotFoundException: If member_id or team_id does not exist
            ResourceNotAllowedException: If team_id does not match the team of the member
        """
        print("Hey")
        member = self._session.get(TeamMember, member_id)
        print("Hey")
        if member == None:
            raise ResourceNotFoundException(f"Member of id={member_id} not found!")

        if member.team_id != team.id:
            raise ResourceNotAllowedException(
                "You must be logged in as the team that the member is a part of to remove that team!"
            )
        self._session.delete(member)
        self._session.commit()
