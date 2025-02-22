"""Service to handle the Session Objects feature"""

# from typing import List, Optional
# from ..models.session_obj import Session_Obj
# from ..services import team
# from .team import Team
# from ..db import db_session
# from fastapi import Depends
# from sqlmodel import Session, select, and_, delete

# import polars as pl
# import datetime as dt

from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Session, select, delete
from ..models.session_obj import Session_Obj
from ..db import db_session

if TYPE_CHECKING:
    from backend.models.team import Team

from .exceptions import (
    ResourceNotFoundException,
    InvalidCredentialsException,
    ResourceNotAllowedException,
)

__authors__ = ["Michelle Nguyen", "Tsering Lama"]


class Session_ObjService:
    """Service that performs actions on Session Objects."""

    def __init__(self, session: Session):
        self._session = session

    def get_session_obj(self, session_id: int) -> Optional[Session_Obj]:
        """Gets a session by ID, including associated teams"""
        return self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

    def get_all_session_objs(self) -> List[Session_Obj]:
        """Gets all sessions"""
        return self._session.exec(select(Session_Obj)).all()

    def create_session_obj(self, session_obj: Session_Obj) -> Session_Obj:
        """Create a new session object in the database.

        Args:
            session_obj (Session_Obj): Session object to create
        Returns:
            Session_Obj: Created session object
        """
        self._session.add(session_obj)
        self._session.commit()
        self._session.refresh(
            session_obj
        )  # Refresh to get any database-generated values
        return session_obj

    def update_session_obj(
        self, session_id: int, session_data: Session_Obj
    ) -> Optional[Session_Obj]:
        """Updates a session and its associated teams"""
        session_obj = self.get_session_obj(session_id)
        if not session_obj:
            return None
        # maybe add catch/exception/error

        session_obj.name = session_data.name
        session_obj.start_time = session_data.start_time
        session_obj.end_time = session_data.end_time

        # If session_data.teams is provided, update the association
        if session_data.teams is not None:
            session_obj.teams.clear()  # Remove existing team associations
            for team in session_data.teams:
                existing_team = self._session.exec(
                    select(Team).where(Team.id == team.id)
                ).first()
                if existing_team:
                    session_obj.teams.append(existing_team)

        self._session.add(session_obj)
        self._session.commit()
        self._session.refresh(session_obj)
        return session_obj

    def delete_session_obj(self, session_id: int) -> bool:
        """Deletes a session but does not delete the teams"""
        session_obj = self.get_session_obj(session_id)
        if not session_obj:
            return False

        self._session.delete(session_obj)
        self._session.commit()
        return True

    def delete_all_session_objs(self):
        """Deletes all sessions but does not delete teams"""
        self._session.exec(delete(Session_Obj))
        self._session.commit()
        return True

    def add_team_to_session(self, session_id: int, team_id: int) -> Session_Obj:
        """Add a team to this session."""
        session = self.get_session_obj(session_id)
        team = self._session.get(Team, team_id)

        if not team:
            raise ResourceNotFoundException("Team", team_id)

        # If team is already in another session, raise error
        if team.session_id and team.session_id != session_id:
            raise ResourceNotAllowedException(
                f"Team {team_id} is already assigned to session {team.session_id}"
            )

        team.session_id = session_id
        self._session.add(team)
        self._session.commit()
        return session

    def remove_team_from_session(self, session_id: int, team_id: int) -> Session_Obj:
        """Remove a team from this session."""
        session = self.get_session_obj(session_id)
        team = self._session.get(Team, team_id)

        if not team:
            raise ResourceNotFoundException("Team", team_id)

        if team.session_id != session_id:
            raise ResourceNotAllowedException(
                f"Team {team_id} is not in session {session_id}"
            )

        team.session_id = None
        self._session.add(team)
        self._session.commit()
        return session

    def get_session_teams(self, session_id: int) -> List["Team"]:
        """Get all teams in this session."""
        session = self.get_session_obj(session_id)
        return session.teams  # SQLModel handles this through the relationship
