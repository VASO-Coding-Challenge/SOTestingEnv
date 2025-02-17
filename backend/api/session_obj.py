"""This API Route handles serving the different sessions"""

from fastapi import APIRouter, Depends

from backend.models.session import Session_Obj
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
def get_all_sessions(
    team: Team = Depends(active_test),
    question_svc: QuestionService = Depends(),
):
    """Get all the questions for the competition"""
    return question_svc.get_questions()


@api.post("", response_model=Session_Obj, tags=["Sessions"])
def add_session(
    team: Team = Depends(active_test),
    question_svc: QuestionService = Depends(),
):
    """Get all the questions for the competition"""
    return question_svc.get_questions()


@api.put("", response_model=Session_Obj, tags=["Sessions"])
def edit_session(
    team: Team = Depends(active_test),
    question_svc: QuestionService = Depends(),
):
    """Get all the questions for the competition"""
    return question_svc.get_questions()


@api.delete("", response_model=Session_Obj, tags=["Sessions"])
def delete_session(
    team: Team = Depends(active_test),
    question_svc: QuestionService = Depends(),
):
    """Get all the questions for the competition"""
    return question_svc.get_questions()
