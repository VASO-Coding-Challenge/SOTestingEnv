from fastapi import APIRouter, Depends, HTTPException, status
from ..models.auth import Token, TokenData, LoginData
from ..services.auth import AuthService
from ..services.team import TeamService


__authors__ = ["Mustafa Aljumayli"]

api = APIRouter(prefix="/api/auth")

openapi_tags = {
    "name": "Auth",
    "description": "These routes are only used for demo/setup confirmation purposes.",
}


@api.post("/login", response_model=Token, tags=["Auth"])
async def authenticate(
    login_data: LoginData,
    auth_service: AuthService = Depends(),
    team_service: TeamService = Depends(),
):
    """Authenticates a team member and returns a JWT Token."""
    team = team_service.get_team(login_data.name)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Team not found",
        )

    token = auth_service.authenticate_and_generate_token(
        name=login_data.name, password=login_data.password, team=team
    )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"access_token": token, "token_type": "bearer"}
