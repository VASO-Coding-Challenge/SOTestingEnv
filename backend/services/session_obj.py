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
        """Updates a session and its associated teams"""
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
        # Unassign teams before deleting session
        teams = self._session.exec(
            select(Team).where(Team.session_id.is_not(None))
        ).all()
        for team in teams:
            team.session_id = None
        self._session.commit()

        self._session.exec(delete(Session_Obj))
        self._session.commit()

    def add_teams_to_session(
        self, session_id: int, team_ids: List[int]
    ) -> SessionPublic:
        """Add teams to an existing session if they exist and are not assigned elsewhere."""

        # Check if session exists
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        # Get teams to be added
        teams = self._session.exec(select(Team).where(Team.id.in_(team_ids))).all()

        # Check if all provided team IDs exist
        found_ids = {team.id for team in teams}
        missing_ids = [tid for tid in team_ids if tid not in found_ids]
        if missing_ids:
            raise ResourceNotFoundException("Team(s)", missing_ids)

        # Identify teams already assigned to another session
        already_assigned = [
            team.id
            for team in teams
            if team.session_id and team.session_id != session_id
        ]

        if already_assigned:
            raise ResourceNotAllowedException(
                f"Team(s) with IDs {already_assigned} are already assigned to another session."
            )

        # Identify teams that are already in the session
        existing_teams = {team.id for team in session_obj.teams}
        duplicate_teams = [tid for tid in team_ids if tid in existing_teams]

        if duplicate_teams:
            raise ResourceNotAllowedException(
                f"Team(s) with IDs {duplicate_teams} are already in this session."
            )

        # Add teams to session
        for team in teams:
            if team.session_id is None:  # Only update unassigned teams
                team.session_id = session_id

        self._session.commit()
        self._session.refresh(session_obj)

        return SessionPublic(
            id=session_obj.id,
            name=session_obj.name,
            start_time=session_obj.start_time,
            end_time=session_obj.end_time,
            teams=[team.id for team in session_obj.teams],
        )

    def remove_teams_from_session(
        self, session_id: int, team_ids: List[int] | None
    ) -> SessionPublic:
        """Remove teams from an existing session if they exist in that session."""

        # Check if session exists
        session_obj = self._session.exec(
            select(Session_Obj).where(Session_Obj.id == session_id)
        ).first()

        if not session_obj:
            raise ResourceNotFoundException("Session", session_id)

        # Get teams to be removed
        teams = self._session.exec(select(Team).where(Team.id.in_(team_ids))).all()

        # Check if all provided team IDs exist
        found_ids = {team.id for team in teams}
        missing_ids = [tid for tid in team_ids if tid not in found_ids]
        if missing_ids:
            raise ResourceNotFoundException("Team(s)", missing_ids)

        # Ensure all teams belong to the session before removal
        not_in_session = [team.id for team in teams if team.session_id != session_id]

        if not_in_session:
            raise ResourceNotAllowedException(
                f"Team(s) with IDs {not_in_session} are not in this session."
            )

        # Remove teams from session (set session_id to None)
        for team in teams:
            team.session_id = None

        self._session.commit()
        self._session.refresh(session_obj)

        return SessionPublic(
            id=session_obj.id,
            name=session_obj.name,
            start_time=session_obj.start_time,
            end_time=session_obj.end_time,
            teams=[team.id for team in session_obj.teams],  # Updated team list
        )
