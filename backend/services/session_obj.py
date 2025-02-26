"""Service to handle the Session Objects feature"""

from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select, delete
from ..models import Team, SessionPublic, Session_Obj
from ..db import db_session
from fastapi import Depends

from .exceptions import ResourceNotFoundException

__authors__ = ["Michelle Nguyen", "Tsering Lama"]


class Session_ObjService:
    """Service that performs actions on Session Objects."""

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def get_session_obj(self, session_id: int) -> SessionPublic:
        """Gets a session by ID, returning a public response format"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        return SessionPublic(
            id=session_obj.id,
            name=session_obj.name,
            start_time=session_obj.start_time,
            end_time=session_obj.end_time,
            teams=[team.id for team in session_obj.teams],
        )

    def get_all_session_objs(self) -> List[SessionPublic]:
        """Gets all sessions"""
        sessions = self._session.exec(select(Session_Obj)).all()

        return [
            SessionPublic(
                id=session.id,
                name=session.name,
                start_time=session.start_time,
                end_time=session.end_time,
                teams=[team.id for team in session.teams],
            )
            for session in sessions
        ]

    def create_session_obj(self, session_data: Session_Obj) -> SessionPublic:
        """Create a new session object in the database with optional team assignments"""
        new_session = Session_Obj(
            name=session_data.name,
            start_time=(
                datetime.fromisoformat(session_data.start_time)
                if isinstance(session_data.start_time, str)
                else session_data.start_time
            ),
            end_time=(
                datetime.fromisoformat(session_data.end_time)
                if isinstance(session_data.end_time, str)
                else session_data.end_time
            ),
        )

        self._session.add(new_session)
        self._session.commit()
        self._session.refresh(new_session)

        if session_data.teams:
            teams = self._session.exec(
                select(Team).where(Team.id.in_(session_data.teams))
            ).all()
            for team in teams:
                team.session_id = new_session.id  # Assign session ID to teams
            self._session.commit()

        return SessionPublic(
            id=new_session.id,
            name=new_session.name,
            start_time=new_session.start_time,
            end_time=new_session.end_time,
            teams=[team.id for team in new_session.teams],  # Return assigned team IDs
        )

    def update_session_obj(
        self, session_id: int, session_data: Session_Obj
    ) -> Optional[SessionPublic]:
        """Update a session object in the database with new details and team assignments"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        # Update session fields
        session_obj.name = session_data.name
        session_obj.start_time = (
            datetime.fromisoformat(session_data.start_time)
            if isinstance(session_data.start_time, str)
            else session_data.start_time
        )
        session_obj.end_time = (
            datetime.fromisoformat(session_data.end_time)
            if isinstance(session_data.end_time, str)
            else session_data.end_time
        )

        # Remove previous team assignments
        for team in session_obj.teams:
            team.session_id = None

        if session_data.teams:
            teams = self._session.exec(
                select(Team).where(Team.id.in_(session_data.teams))
            ).all()
            for team in teams:
                team.session_id = session_id  # Assign session ID to new teams

        self._session.commit()
        self._session.refresh(session_obj)

        return SessionPublic(
            id=session_obj.id,
            name=session_obj.name,
            start_time=session_obj.start_time,
            end_time=session_obj.end_time,
            teams=[team.id for team in session_obj.teams],  # Return assigned team IDs
        )

    def delete_session_obj(self, session_id: int) -> bool:
        """Deletes a session object"""
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            return False

        # Unassign teams before deleting session
        for team in session_obj.teams:
            team.session_id = None
        self._session.commit()

        self._session.delete(session_obj)
        self._session.commit()
        return True

    def delete_all_session_objs(self):
        """Deletes all session objects"""
        # Unassign teams from all sessions
        self._session.exec(select(Team)).update({Team.session_id: None})
        self._session.commit()
        # Delete all sessions
        self._session.exec(delete(Session_Obj))
        self._session.commit()
