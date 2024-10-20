from fastapi import APIRouter, Depends
from ..models.team import Team
from ..services.team import TeamService

__authors__ = ["Mustafa Aljumayli"]

api = APIRouter(prefix="/api/test/teams")

openapi_tags = {
    "name": "Teams",
    "description": "These routes are only used for demo/setup confirmation purposes.",
}


@api.get("/", tags=["Teams"])
async def get_teams(team_service: TeamService = Depends()):
    """Gets all teams"""
    return team_service.get_all_teams()


@api.get("/id/{id}", tags=["Teams"])
async def get_team(id: int, team_service: TeamService = Depends()) -> Team:
    """Gets the team object"""
    return team_service.get_team(id)


@api.get("/name/{name}", tags=["Teams"])
async def get_team(name: str, team_service: TeamService = Depends()) -> Team:
    """Gets the team by name"""
    return team_service.get_team(name)
