from sqlmodel import Session
from datetime import time, timedelta

from backend.models.team import Team
from backend.services.auth import AuthService
from backend.services.team import TeamService
from backend.db import engine

__authors__ = ["Mustafa Aljumayli"]


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""

    auth_service = AuthService(session)
    team_service = TeamService(session)

    team1 = Team(
        id=1,
        name="B1",
        password=team_service.generate_password(),
        start_time=time(9, 0),
        end_time=time(9, 0),
        login_time=timedelta(minutes=30),
    )
    team2 = Team(
        id=2,
        name="B2",
        password=team_service.generate_password(),
        start_time=time(9, 0),
        end_time=time(9, 0),
        login_time=timedelta(minutes=30),
    )
    team3 = Team(
        id=3,
        name="B3",
        password=team_service.generate_password(),
        start_time=time(9, 0),
        end_time=time(9, 0),
        login_time=timedelta(minutes=30),
    )

    # Add the teams to the session
    session.add_all([team1, team2, team3])
    session.commit()
