"""This API Route handles question submission and scoring"""

from typing import List
from fastapi import APIRouter, Depends
from ..models import Team, Submission, ConsoleLog
from ..services.submissions import SubmissionService
from .auth import active_test
import sys

__authors__ = ["Nicholas Almy"m "Michelle Nguyen"]

openapi_tags = {
    "name": "Submissions",
    "description": "Routes for Submission management",
}

api = APIRouter(prefix="/api/submissions")


@api.get("/", response_model=List[int], tags=["Submissions"])
def get_submissions(t_num: int):
    """Get a specific team's submissions."""
    return SubmissionService.get_problems_list()


@api.get("/", response_model=List[int], tags=["Submissions"])
def get_all_submissions():
    """Get all team's submissions."""
    return SubmissionService.get_problems_list()


@api.get("/", response_model=List[int], tags=["Submissions"])
def get_specific_submission(t_num: int):
    """Get all team's submissions."""
    return SubmissionService.get_problems_list()


@api.post("/submit", response_model=ConsoleLog, tags=["Submissions"])
def submit_and_run(
    submission: Submission,
    team: Team = Depends(active_test),
    submission_svc: SubmissionService = Depends(),
) -> ConsoleLog:
    """Store and sample grade a submission."""
    return submission_svc.submit_and_run(team, submission)
