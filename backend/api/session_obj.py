"""This API Route handles serving the different sessions"""

from fastapi import APIRouter, Depends, HTTPException
from backend.models.session_obj import Session_Obj
from backend.services.session_obj import Session_ObjService
from ..models import QuestionsPublic, Team
from ..services.questions import QuestionService
from .auth import active_test

import sys

__authors__ = ["Michelle Nguyen", "Tsering Lama"]

openapi_tags = {
    "name": "Session",
    "description": "Routes for Session retrieval",
}


api = APIRouter(prefix="/api/sessions", tags=["Sessions"])


@api.get("/", response_model=List[Session_Obj])
def get_all_sessions(session_svc: Session_ObjService = Depends()):
    """Get all sessions along with their associated teams"""
    return session_svc.get_all_session_objs()


@api.get("/{session_id}", response_model=Session_Obj)
def get_session(session_id: int, session_svc: Session_ObjService = Depends()):
    """Get a specific session by ID, including associated teams"""
    session_obj = session_svc.get_session_obj(session_id)
    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")
    return session_obj


@api.post("/", response_model=Session_Obj)
def create_session(
    session_obj: Session_Obj, session_svc: Session_ObjService = Depends()
):
    """Create a new session"""
    return session_svc.create_session_obj(session_obj)


@api.put("/{session_id}", response_model=Session_Obj)
def update_session(
    session_id: int,
    session_obj: Session_Obj,
    session_svc: Session_ObjService = Depends(),
):
    """Update a session and modify its associated teams"""
    updated_session = session_svc.update_session_obj(session_id, session_obj)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return updated_session


@api.delete("/{session_id}")
def delete_session(session_id: int, session_svc: Session_ObjService = Depends()):
    """Delete a specific session but keep the teams intact"""
    success = session_svc.delete_session_obj(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@api.delete("/")
def delete_all_sessions(session_svc: Session_ObjService = Depends()):
    """Delete all sessions but keep the teams intact"""
    session_svc.delete_all_session_objs()
    return {"message": "All sessions deleted successfully"}
