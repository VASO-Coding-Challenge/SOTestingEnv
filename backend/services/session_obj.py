"""Service to handle the Session Objects feature"""

from typing import List, Optional
from ..models.session_obj import Session_Obj
from ..services import team
from .team import Team
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
        """Creates a new session"""
        self._session.add(session_obj)
        self._session.commit()
        self._session.refresh(session_obj)
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
