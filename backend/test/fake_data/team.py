from sqlmodel import Session
from datetime import datetime, timedelta

from backend.models.team import Team
from backend.services.passwords import PasswordService
from backend.db import engine

__authors__ = ["Mustafa Aljumayli", "Andrew Lockard"]

team1 = Team(
    id=1,
    name="B1",
    password=PasswordService.generate_password(),
    start_time=datetime.now() + timedelta(hours=1),
    end_time=datetime.now() + timedelta(hours=1, minutes=30),
    active_JWT=False,
)
team2 = Team(
    id=2,
    name="B2",
    password=PasswordService.generate_password(),
    start_time=datetime.now() + timedelta(hours=1),
    end_time=datetime.now() + timedelta(hours=1, minutes=30),
    active_JWT=False,
)
team3 = Team(
    id=3,
    name="B3",
    password=PasswordService.generate_password(),
    start_time=datetime.now() + timedelta(hours=2),
    end_time=datetime.now() + timedelta(hours=3),
    active_JWT=False,
)

teams = [team1, team2, team3]


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""
    for team in teams:
        session.add(team)
    session.commit()
