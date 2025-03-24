"""API Routes associated with Teams and TeamMember data objects"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException

from backend.services.exceptions import ResourceNotAllowedException
from ..models.team import TeamPublic, Team, TeamData
from ..services.team import TeamService
from ..models.team_members import TeamMemberCreate, TeamMemberPublic
from .auth import authed_team

__authors__ = ["Andrew Lockard", "Mustafa Aljumayli", "Tsering Lama"]

api = APIRouter(prefix="/api/team")

openapi_tags = {"name": "Teams", "description": "Routes for Teams and TeamMembers."}


@api.get("", response_model=TeamPublic, tags=["Teams"])
def get_team(team: Team = Depends(authed_team)) -> TeamPublic:
    """Gets the currently logged in team"""
    return team


@api.get("/members", response_model=list[TeamMemberPublic], tags=["Teams"])
def get_team_members(
    team_id: int = None,
    team: Team = Depends(authed_team),
    team_svc: TeamService = Depends(),
):
    """
    Gets all the team members for a team
    If team_id is provided, returns members for that specific team
    Otherwise, returns members for the currently authenticated team
    """
    if team_id:
        # If a specific team ID is requested, get that team
        requested_team = team_svc.get_team(team_id)
        return requested_team.members
    else:
        # Otherwise return the current authenticated team's members
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

@api.get("/all", response_model=list[TeamPublic], tags=["Teams"])
def get_all_teams(
    team_svc: TeamService = Depends(),
) -> list[TeamPublic]:
    """Retrieve all teams"""
    return team_svc.get_all_teams()


@api.post("", response_model=TeamPublic, tags=["Teams"])
def create_team(
    team_data: TeamData, team_svc: TeamService = Depends()
) -> TeamPublic:
    """Create a new team"""
    try:
        return team_svc.create_team(team_data)
    except ResourceNotAllowedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@api.post("/batch", response_model=list[TeamPublic], tags=["Teams"])
def create_batch_teams(
    team_names: List[str], team_template: TeamData, team_svc: TeamService = Depends()
) -> list[TeamPublic]:
    """Create multiple teams at once based on a template and provided names"""
    try:
        teams = team_svc.create_batch_teams(team_names, team_template)
        return teams
    except ResourceNotAllowedException as e:
        raise HTTPException(status_code=409, detail=str(e))


@api.delete("/{team_id}", tags=["Teams"])
def delete_team(team_id: int, team_svc: TeamService = Depends()):
    """Delete a specific team"""
    success = team_svc.delete_team_by_id(team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": f"Team {team_id} deleted successfully"}


@api.delete("", tags=["Teams"])
def delete_all_teams(team_svc: TeamService = Depends()):
    """Delete all teams"""
    team_svc.delete_all_teams()
    return {"message": "All teams deleted successfully"}