"""This API Route handles serving the questions and documentation"""

from fastapi import APIRouter, Depends
from ..models import QuestionsPublic, Team
from ..services.questions import QuestionService
from .auth import active_test
import sys

__authors__ = ["Nicholas Almy"]

openapi_tags = {
    "name": "Questions",
    "description": "Routes for Question retrieval",
}

api = APIRouter(prefix="/api/questions")


@api.get("", response_model=QuestionsPublic, tags=["Questions"])
def get_questions(
    team: Team = Depends(active_test),
    question_svc: QuestionService = Depends(),
):
    """Get all the questions for the competition"""
    return question_svc.get_questions()
