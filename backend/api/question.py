"""This API Route handles serving the questions and documentation"""

from fastapi import APIRouter, Depends, HTTPException
from ..models import QuestionsPublic, Team
from ..services.questions import QuestionService
from ..services.auth import AuthService
from .auth import authed_team

__authors__ = ["Nicholas Almy"]

openapi_tags = {
    "name": "Questions",
    "description": "Routes for Question retrieval",
}

api = APIRouter(prefix="/api/questions")


@api.get("/questions", response_model=QuestionsPublic, tags=["Questions"])
def get_questions(team: Team = Depends(authed_team)):
    """Get all the questions for the competition"""
    try:
        AuthService.authenticate_team_time(team)
    except Exception as e:
        raise HTTPException(401, str(e))
    question_svc = QuestionService()
    return question_svc.get_questions()
