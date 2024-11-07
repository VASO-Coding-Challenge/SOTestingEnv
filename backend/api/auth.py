from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.auth import Token, TokenData, LoginData
from ..models.team import Team

from ..services.auth import AuthService
from ..services.team import TeamService
from ..services.exceptions import InvalidCredentialsException

__authors__ = ["Mustafa Aljumayli", "Andrew Lockard"]

api = APIRouter(prefix="/api/auth")

bearer_scheme = HTTPBearer()

openapi_tags = {
    "name": "Auth",
    "description": "Routes used for login and other JWT concerns",
}


def authed_team(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(),
) -> Team:
    """Retreives the current team object associated with the sent JWT.
    Designed to be dependency injected into API definition"""
    token = credentials.credentials  # This extracts the token from the header
    return auth_service.get_team_from_token(token)

def active_test(
        credientials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        auth_service: AuthService = Depends(),
) -> Team:
    """Retrieves the current team object like authed_team, but will also throw a 403 error if the
    student's test is not currently active."""
    token = credientials.credentials
    team = auth_service.get_team_from_token(token)
    auth_service.authenticate_team_time(team)
    return Team


@api.post("/login", response_model=Token, tags=["Auth"])
async def authenticate(
    login_data: LoginData,
    auth_service: AuthService = Depends(),
    team_service: TeamService = Depends(),
) -> Token:
    """Returns a JWT Token for an authorized user."""
    token = auth_service.authenticate_team(
        name=login_data.name,
        password=login_data.password,
        team_service=team_service,
    )

    return token


@api.get("/me", response_model=TokenData, tags=["Auth"])
async def get_current_team(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(),
):
    """
    Retrieves the currently logged-in team using their JWT token.
    """
    token = credentials.credentials  # This extracts the token from the header

    token_data = auth_service.decode_token(token)

    if not token_data:
        raise InvalidCredentialsException("Token is Invalid")

    return token_data


@api.post("/logout", tags=["Auth"])
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    auth_service: AuthService = Depends(),
    team_service: TeamService = Depends(),
):
    """
    Log out the current team by deactivating the JWT.
    """
    token = credentials.credentials
    token_data = auth_service.decode_token(token)

    # Fetch the team and set active_JWT to False
    team = team_service.get_team(token_data.id)
    if team:
        team.active_JWT = False
        auth_service._session.add(team)
        auth_service._session.commit()
    return {"message": "Logged out successfully"}
