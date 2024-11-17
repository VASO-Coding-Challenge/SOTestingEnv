"""This API Route handles question submission and scoring"""

from fastapi import APIRouter, Depends
from ..models import Team, Submission, ConsoleLog
from ..services.submissions import SubmissionService
from .auth import active_test

__authors__ = ["Nicholas Almy"]

openapi_tags = {
    "name": "Submissions",
    "description": "Routes for Submission management",
}

api = APIRouter(prefix="/api/submissions")


@api.post("/submit", response_model=ConsoleLog, tags=["Submissions"])
def submit_and_run(
    submission: Submission,
    team: Team = Depends(active_test),
    submission_svc: SubmissionService = Depends(),
) -> ConsoleLog:
    """Store and sample grade a submission."""
    return submission_svc.submit_and_run(team, submission)
