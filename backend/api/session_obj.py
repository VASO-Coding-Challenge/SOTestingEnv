"""This API Route handles serving the different sessions"""

from fastapi import APIRouter, Depends

from backend.models.session_obj import Session_Obj
from backend.services.session_obj import Session_ObjService
from ..models import QuestionsPublic, Team
from ..services.questions import QuestionService
from .auth import active_test
import sys

__authors__ = [""]

openapi_tags = {
    "name": "Session",
    "description": "Routes for Session retrieval",
}

api = APIRouter(prefix="/api/sessions")


@api.get("", response_model=Session_Obj, tags=["Sessions"])
def get_session(
    session_obj: Session_Obj = Depends(active_test),
    session_svc: Session_ObjService = Depends(),
):
    """Get a specific session"""
    return session_svc.get_session_obj


@api.get("", response_model=Session_Obj, tags=["Sessions"])
def get_all_sessions(
    session_obj: Session_Obj = Depends(active_test),
    session_svc: Session_ObjService = Depends(),
):
    """Get all sessions"""
    return session_svc.get_all_session_objs()


@api.post("", response_model=Session_Obj, tags=["Sessions"])
def create_session(
    team: Team = Depends(active_test),
    question_svc: Session_ObjService = Depends(),
):
    """Creates a new session"""
    return question_svc.create_session_obj


@api.put("/sessions/{session_id}", response_model=Session_Obj, tags=["Sessions"])
def update_session(
    team: Team = Depends(active_test),
    question_svc: Session_ObjService = Depends(),
):
    """Updates a specific session"""
    return question_svc.update_session_obj


@api.delete("/sessions/{session_id}", response_model=None, tags=["Sessions"])
def delete_session(
    team: Team = Depends(active_test),
    session_svc: Session_ObjService = Depends(),
    # session_id: int,
    # team: Team = Depends(authed_team),
    # team_svc: TeamService = Depends()
):
    """Delete a specific session"""
    return session_svc.delete_session_obj


@api.delete("/sessions", response_model=None, tags=["Sessions"])
def delete_session(
    team: Team = Depends(active_test),
    session_svc: Session_ObjService = Depends(),
):
    """Deletes all sessions"""
    return session_svc.delete_all_session_objs
