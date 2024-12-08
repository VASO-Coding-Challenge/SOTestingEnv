from sqlmodel import Session
from datetime import datetime, timedelta

import pytest

from backend.models.team import Team
from backend.services.passwords import PasswordService
from backend.db import engine

__authors__ = ["Mustafa Aljumayli", "Nicholas Almy", "Andrew Lockard"]

team1 = Team(
    id=1,
    name="B1",
    password="a-b-c",
    start_time=datetime.now() - timedelta(minutes=30),
    end_time=datetime.now() + timedelta(minutes=30),
)
team2 = Team(
    id=2,
    name="B2",
    password="a-b-c",
    start_time=datetime.now() + timedelta(minutes=2),
    end_time=datetime.now() + timedelta(hours=1, minutes=2),
)
team3 = Team(
    id=3,
    name="B3",
    password="a-b-c",
    start_time=datetime.now() + timedelta(hours=1),
    end_time=datetime.now() + timedelta(hours=2),
)


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""
    # Add the teams to the session
    session.add_all([team1, team2, team3])


@pytest.fixture(scope="function", autouse=True)
def fake_team_fixture(session: Session):
    create_fake_teams(session)
    session.commit()
