"""This API Route handles question submission and scoring"""

from fastapi import APIRouter, Depends
from ..models import QuestionsPublic, Team, Submission, ConsoleLog
from ..services.questions import QuestionService
from .auth import active_test

__authors__ = ["Nicholas Almy"]

openapi_tags = {
    "name": "Submissions",
    "description": "Routes for Submission management",
}

api = APIRouter(prefix="/api/submissions")


@api.get("/submit", response_model=QuestionsPublic, tags=["Submissions"])
def get_questions(
    submission: Submission = Depends(active_test),
    team: Team = Depends(active_test),
    submission_svc: QuestionService = Depends(),
) -> ConsoleLog:
    """Store and sample grade a submission."""
    return submission_svc.submit(submission)
