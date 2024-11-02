from sqlmodel import Session
from datetime import datetime, timedelta

from backend.models.team import Team
from backend.services.auth import AuthService
from backend.services.passwords import PasswordService
from backend.db import engine

__authors__ = ["Mustafa Aljumayli", "Nicholas Almy"]

time1 = datetime(year=2024, month=11, day=1, hour=9, minute=0)
time2 = datetime(year=2024, month=11, day=1, hour=10, minute=0)

team1 = Team(
    id=1,
    name="B1",
    password="a-b-c",
    start_time=time1,
    end_time=time2,
    active_JWT=False,
)
team2 = Team(
    id=2,
    name="B2",
    password="a-b-c",
    start_time=time1,
    end_time=time2,
    active_JWT=False,
)
team3 = Team(
    id=3,
    name="B3",
    password="a-b-c",
    start_time=time1,
    end_time=time2,
    active_JWT=False,
)


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""
    # Add the teams to the session
    session.add_all([team1, team2, team3])
    session.commit()
