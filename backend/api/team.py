"""API Routes associated with Teams and TeamMember data objects"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from ..models.team import TeamPublic, Team, TeamData
from ..services.team import TeamService
from ..services.submissions import SubmissionService
from ..models.team_members import TeamMemberCreate, TeamMemberPublic
from .auth import authed_team

__authors__ = ["Andrew Lockard", "Mustafa Aljumayli", "Tsering Lama"]

api = APIRouter(prefix="/api/team")

openapi_tags = {"name": "Teams", "description": "Routes for Teams and TeamMembers."}


@api.get("", response_model=TeamPublic, tags=["Teams"])
def get_team(team: Team = Depends(authed_team)) -> TeamPublic:
    """Gets the currently logged in team"""
    return team


@api.get("/all", response_model=list[TeamPublic], tags=["Teams"])
def get_all_teams(team_svc: TeamService = Depends()):
    """Gets all the teams"""
    return team_svc.get_all_teams()


@api.get("/members", response_model=list[TeamMemberPublic], tags=["Teams"])
def get_team_members(team: Team = Depends(authed_team)):
    """Gets all the team members for a team"""
    return team.members


@api.post("/members", response_model=TeamMemberPublic, tags=["Teams"])
def add_team_member(
    new_member: TeamMemberCreate,
    team: Team = Depends(authed_team),
    team_svc: TeamService = Depends(),
):
    """Adds a team member to the currently logged in team."""
    return team_svc.add_team_member(new_member, team)


@api.delete("/members/{member_id}", response_model=None, tags=["Teams"])
def delete_team_member(
    member_id: int, team: Team = Depends(authed_team), team_svc: TeamService = Depends()
):
    """Deletes a team member from the currenlty logged in team."""
    team_svc.delete_team_member(member_id, team)
    return {"message": f"Team Member {member_id} deleted successfully"}


# reorder this later

# @api.get("/all", response_model=list[TeamPublic], tags=["Teams"])
# def get_all_teams(
#     team_svc: TeamService = Depends(),
# ) -> list[TeamPublic]:
#     """Retrieve all teams"""
#     return team_svc.get_all_teams()


@api.post("", response_model=TeamPublic, tags=["Teams"])
def create_team(team_data: TeamData, team_svc: TeamService = Depends()) -> TeamPublic:
    """Create a new team"""
    return team_svc.create_team(team_data)


@api.post("/batch/{count}", response_model=list[TeamPublic], tags=["Teams"])
def create_batch_teams(
    count: int, team_template: TeamData, team_svc: TeamService = Depends()
) -> list[TeamPublic]:
    """Create multiple teams at once based on a template

    Args:
        count: Number of teams to create
        team_template: Template for the teams with base name, password, etc.
    """
    return team_svc.create_batch_teams(count, team_template)


# @api.delete("/{team_id}", tags=["Teams"])
# def delete_team(team_id: int, team_svc: TeamService = Depends()):
#     """Delete a specific team"""
#     success = team_svc.delete_team_by_id(team_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Team not found")
#     return {"message": f"Team {team_id} deleted successfully"}


# @api.delete("", tags=["Teams"])
# def delete_all_teams(team_svc: TeamService = Depends()):
#     """Delete all teams"""
#     team_svc.delete_all_teams()
#     return {"message": "All teams deleted successfully"}


# @api.delete("/{team_id}", tags=["Teams"])
# def delete_team(team_id: int, team_svc: TeamService = Depends()):
#     """Delete a specific team"""
#     success_delete = SubmissionService.delete_submissions(team_name)
#     success = team_svc.delete_team_by_id(team_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Team not found")
#     return {"message": f"Team {team_id} deleted successfully"}


# @api.delete("", tags=["Teams"])
# def delete_all_teams(team_svc: TeamService = Depends()):
#     """Delete all teams"""
#     # loop through all teams then delete
#     # success_delete = SubmissionService.delete_submissions(team_name)
#     team_svc.delete_all_teams()
#     return {"message": "All teams deleted successfully"}


# @api.delete("/{team_id}", tags=["Teams"])
# def delete_team(team_id: int, team_svc: TeamService = Depends()):
#     """Delete a specific team"""
#     team = team_svc.get_team_by_id(team_id)

#     if not team:
#         raise HTTPException(status_code=404, detail="Team not found")

#     success_delete_submissions = SubmissionService.delete_submissions(team.name)
#     if not success_delete_submissions:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to delete submissions for team {team.name}"
#         )

#     success_delete_team = team_svc.delete_team_by_id(team_id)
#     if not success_delete_team:
#         raise HTTPException(
#             status_code=500, detail=f"Failed to delete team {team.name}"
#         )

#     return {"message": f"Team {team.name} (ID: {team_id}) deleted successfully"}


# @api.delete("", tags=["Teams"])
# def delete_all_teams(team_svc: TeamService = Depends()):
#     """Delete all teams"""
#     teams = team_svc.get_all_teams()

#     for team in teams:
#         success_delete_submissions = SubmissionService.delete_submissions(
#             team.name
#         )  # Use team name
#         if not success_delete_submissions:
#             raise HTTPException(
#                 status_code=500,
#                 detail=f"Failed to delete submissions for team {team.name}",
#             )

#     team_svc.delete_all_teams()
#     return {"message": "All teams and their submissions deleted successfully"}


@api.delete("/{team_id}", tags=["Teams"])
def delete_team(team_id: int, team_svc: TeamService = Depends()):
    """Delete a specific team"""
    team_name = team_svc.get_team_name_by_id(team_id)

    if not team_name:
        raise HTTPException(status_code=404, detail="Team not found")

    success_delete_submissions = SubmissionService.delete_submissions(team_name)
    if not success_delete_submissions:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete submissions for team {team_name}"
        )

    success_delete_team = team_svc.delete_team_by_id(team_id)
    if not success_delete_team:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete team {team_name}"
        )

    return {"message": f"Team {team_name} (ID: {team_id}) deleted successfully"}


@api.delete("", tags=["Teams"])
def delete_all_teams(team_svc: TeamService = Depends()):
    """Delete all teams"""
    teams = team_svc.get_all_teams()

    for team in teams:
        team_name = team.name
        success_delete_submissions = SubmissionService.delete_submissions(team_name)
        if not success_delete_submissions:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete submissions for team {team_name}",
            )

    team_svc.delete_all_teams()
    return {"message": "All teams and their submissions deleted successfully"}
