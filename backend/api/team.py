"""API Routes associated with Teams and TeamMember data objects"""

from typing import List
from fastapi import APIRouter, Depends
from ..models.team import TeamPublic, Team
from ..services.team import TeamService
from ..models.team_members import TeamMemberCreate, TeamMemberPublic
from .auth import authed_team

__authors__ = ["Andrew Lockard", "Mustafa Aljumayli"]

api = APIRouter(prefix="/api/team")

openapi_tags = {"name": "Teams", "description": "Routes for Teams and TeamMembers."}


# TODO: Update these to follow better conventions
@api.get("", response_model=list[TeamPublic], tags=["Teams"])
async def get_teams(team_service: TeamService = Depends()) -> List[TeamPublic]:
    """Gets all teams"""
    return team_service.get_all_teams()


@api.get("/id/{id}", response_model=TeamPublic, tags=["Teams"])
async def get_team(id: int, team_service: TeamService = Depends()) -> TeamPublic:
    """Gets the team object"""
    return team_service.get_team(id)


@api.get("/name/{name}", response_model=TeamPublic, tags=["Teams"])
async def get_team(name: str, team_service: TeamService = Depends()) -> TeamPublic:
    """Gets the team by name"""
    return team_service.get_team(name)


@api.get("/members", response_model=list[TeamMemberPublic], tags=["Teams"])
def get_team_members(
    team: Team = Depends(authed_team), team_svc: TeamService = Depends()
):
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
