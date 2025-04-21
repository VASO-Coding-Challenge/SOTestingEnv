"""This API Route handles question submission and scoring"""

from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from ..models import Team, Submission, ConsoleLog
from ..services.submissions import SubmissionService
from .auth import active_test
import sys

__authors__ = ["Nicholas Almy", "Michelle Nguyen"]

openapi_tags = {
    "name": "Submissions",
    "description": "Routes for Submission management",
}

api = APIRouter(prefix="/api/submissions")


@api.get("/all", response_model=Dict[str, Dict[int, str]], tags=["Submissions"])
def get_all_submissions():
    """Get all teams' submissions across all problems."""
    return SubmissionService.get_all_submissions()


@api.get("/team/{team_name}", response_model=Dict[int, str], tags=["Submissions"])
def get_team_submissions(team_name: str):
    """Get a specific team's submissions across all problems."""
    try:
        return SubmissionService.get_team_submissions(team_name)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/team/{team_name}/problem/{p_num}", response_model=str, tags=["Submissions"])
def get_specific_submission(team_name: str, p_num: int):
    """Get a specific team's submission for a specific problem."""
    try:
        return SubmissionService.get_specific_submission(team_name, p_num)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.post("/submit", response_model=ConsoleLog, tags=["Submissions"])
def submit_and_run(
    submission: Submission,
    team: Team = Depends(active_test),
    submission_svc: SubmissionService = Depends(),
) -> ConsoleLog:
    """Store and sample grade a submission."""
    return submission_svc.submit_and_run(team, submission)


@api.delete("", tags=["Submissions"])
def delete_all_submissions(
    submission_svc: SubmissionService = Depends(),
):
    """Delete all submissions for a team."""
    try:
        submission_svc.delete_all_submissions()
        return {"message": "All submissions deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
