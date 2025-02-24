"""Service to handle the Session Objects feature"""

from typing import List, Optional
from sqlmodel import Session, select, delete
from ..db import db_session
from ..models import Team, SessionPublic, Session_Obj

from .exceptions import (
    ResourceNotFoundException,
    ResourceNotAllowedException,
)

__authors__ = ["Michelle Nguyen", "Tsering Lama"]


class Session_ObjService:
    """Service that performs actions on Session Objects."""

    def __init__(self, session: Session):
        self._session = session

    def get_session_obj(self, session_id: int) -> Optional[SessionPublic]:
        """Gets a session by ID, returning a public response format"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        return SessionPublic.model_validate(session_obj)

    def get_all_session_objs(self) -> List[SessionPublic]:
        """Gets all sessions"""
        sessions = self._session.exec(select(Session_Obj)).all()
        return [SessionPublic.model_validate(session) for session in sessions]

    def create_session_obj(self, session_obj: Session_Obj) -> SessionPublic:
        """Create a new session object in the database."""
        self._session.add(session_obj)
        self._session.commit()
        self._session.refresh(session_obj)
        return SessionPublic.model_validate(session_obj)

    def update_session_obj(
        self, session_id: int, session_data: Session_Obj
    ) -> Optional[SessionPublic]:
        """Updates a session and its associated teams"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        session_obj.name = session_data.name
        session_obj.start_time = session_data.start_time
        session_obj.end_time = session_data.end_time

        # Update teams if provided
        if session_data.teams is not None:
            session_obj.teams.clear()
            for team in session_data.teams:
                existing_team = self._session.exec(
                    select(Team).where(Team.id == team.id)
                ).first()
                if existing_team:
                    session_obj.teams.append(existing_team)

        self._session.commit()
        self._session.refresh(session_obj)
        return SessionPublic.model_validate(session_obj)

    def delete_session_obj(self, session_id: int) -> bool:
        """Deletes a session but does not delete the teams"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            return False

        self._session.delete(session_obj)
        self._session.commit()
        return True

    def delete_all_session_objs(self) -> bool:
        """Deletes all sessions but does not delete teams"""
        self._session.exec(delete(Session_Obj))
        self._session.commit()
        return True

    def add_team_to_session(self, session_id: int, team_id: int) -> SessionPublic:
        """Add a team to this session."""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()
        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        team = self._session.get(Team, team_id)
        if not team:
            raise ResourceNotFoundException("Team", team_id)

        # If team is already in another session, raise error
        if team.session_id and team.session_id != session_id:
            raise ResourceNotAllowedException(
                f"Team {team_id} is already assigned to session {team.session_id}"
            )

        team.session_id = session_id
        self._session.commit()
        return SessionPublic.model_validate(session_obj)

    def remove_team_from_session(self, session_id: int, team_id: int) -> SessionPublic:
        """Remove a team from this session."""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()
        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        team = self._session.get(Team, team_id)
        if not team:
            raise ResourceNotFoundException("Team", team_id)

        if team.session_id != session_id:
            raise ResourceNotAllowedException(
                f"Team {team_id} is not in session {session_id}"
            )

        team.session_id = None
        self._session.commit()
        return SessionPublic.model_validate(session_obj)

    def get_session_teams(self, session_id: int) -> List[Team]:
        """Get all teams in this session."""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()
        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        return session_obj.teams  # SQLModel handles this through the relationship
