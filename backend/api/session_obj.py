"""API Routes for managing session objects"""

# from typing import List
# from fastapi import APIRouter, Depends, HTTPException
# from ..models.session_obj import Session_Obj, SessionPublic
# from ..services.session_obj import Session_ObjService

# __authors__ = ["Michelle Nguyen", "Tsering Lama"]

# api = APIRouter(prefix="/api/sessions")

# openapi_tags = {
#     "name": "Sessions",
#     "description": "Routes for retrieving and managing sessions.",
# }


# @api.get("/", response_model=List[SessionPublic], tags=["Sessions"])
# def get_all_sessions(session_svc: Session_ObjService = Depends()):
#     """Retrieve all sessions along with their associated teams"""
#     return session_svc.get_all_session_objs()


# @api.get("/{session_id}", response_model=SessionPublic, tags=["Sessions"])
# def get_session(session_id: int, session_svc: Session_ObjService = Depends()):
#     """Retrieve a specific session by ID, including associated teams"""
#     session_obj = session_svc.get_session_obj(session_id)
#     if not session_obj:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return session_obj


# @api.post("/", response_model=SessionPublic, tags=["Sessions"])
# def create_session(
#     session_obj: Session_Obj, session_svc: Session_ObjService = Depends()
# ):
#     """Create a new session"""
#     return session_svc.create_session_obj(session_obj)


# @api.put("/{session_id}", response_model=SessionPublic, tags=["Sessions"])
# def update_session(
#     session_id: int,
#     session_obj: Session_Obj,
#     session_svc: Session_ObjService = Depends(),
# ):
#     """Update a session and modify its associated teams"""
#     updated_session = session_svc.update_session_obj(session_id, session_obj)
#     if not updated_session:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return updated_session


# @api.delete("/{session_id}", response_model=None, tags=["Sessions"])
# def delete_session(session_id: int, session_svc: Session_ObjService = Depends()):
#     """Delete a specific session but keep the teams intact"""
#     success = session_svc.delete_session_obj(session_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return {"message": "Session deleted successfully"}


# @api.delete("/", response_model=None, tags=["Sessions"])
# def delete_all_sessions(session_svc: Session_ObjService = Depends()):
#     """Delete all sessions but keep the teams intact"""
#     session_svc.delete_all_session_objs()
#     return {"message": "All sessions deleted successfully"}

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

# from ..db import get_session
from backend.db import db_session as get_session
from ..models.session_obj import Session_Obj, SessionPublic
from ..services.session_obj import Session_ObjService

__authors__ = ["Michelle Nguyen", "Tsering Lama"]

api = APIRouter(prefix="/api/sessions")

openapi_tags = {
    "name": "Sessions",
    "description": "Routes for retrieving and managing sessions.",
}


@api.get("/", response_model=List[SessionPublic], tags=["Sessions"])
def get_all_sessions(session: Session = Depends(get_session)):
    """Retrieve all sessions along with their associated teams"""
    session_svc = Session_ObjService(session)
    return session_svc.get_all_session_objs()


@api.get("/{session_id}", response_model=SessionPublic, tags=["Sessions"])
def get_session(session_id: int, session: Session = Depends(get_session)):
    """Retrieve a specific session by ID, including associated teams"""
    session_svc = Session_ObjService(session)
    session_obj = session_svc.get_session_obj(session_id)
    return session_obj


@api.post("/", response_model=SessionPublic, tags=["Sessions"])
def create_session(session_obj: Session_Obj, session: Session = Depends(get_session)):
    """Create a new session"""
    session_svc = Session_ObjService(session)
    return session_svc.create_session_obj(session_obj)


@api.put("/{session_id}", response_model=SessionPublic, tags=["Sessions"])
def update_session(
    session_id: int,
    session_obj: Session_Obj,
    session: Session = Depends(get_session),
):
    """Update a session and modify its associated teams"""
    session_svc = Session_ObjService(session)
    updated_session = session_svc.update_session_obj(session_id, session_obj)
    if not updated_session:
        raise HTTPException(status_code=404, detail="Session not found")
    return updated_session


@api.delete("/{session_id}", tags=["Sessions"])
def delete_session(session_id: int, session: Session = Depends(get_session)):
    """Delete a specific session but keep the teams intact"""
    session_svc = Session_ObjService(session)
    success = session_svc.delete_session_obj(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@api.delete("/", tags=["Sessions"])
def delete_all_sessions(session: Session = Depends(get_session)):
    """Delete all sessions but keep the teams intact"""
    session_svc = Session_ObjService(session)
    session_svc.delete_all_session_objs()
    return {"message": "All sessions deleted successfully"}
