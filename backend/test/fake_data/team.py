from sqlmodel import Session
from datetime import datetime, timedelta

import pytest

from backend.models.team import Team
from backend.services.passwords import PasswordService
from backend.db import engine
from .session_obj import fake_session_fixture

__authors__ = [
    "Mustafa Aljumayli",
    "Nicholas Almy",
    "Andrew Lockard",
    "Ivan Wu",
    "Michelle Nguyen",
]


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""
    # Add the teams to the session
    team1 = Team(
        id=1,
        name="B1",
        password="a-b-c",
        session_id=1,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
    )
    team2 = Team(
        id=2,
        name="B2",
        password="a-b-c",
        session_id=2,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
    )
    team3 = Team(
        id=3,
        name="B3",
        password="a-b-c",
        session_id=None,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
    )
    team4 = Team(
        id=4,
        name="B4",
        password="a-b-c",
        session_id=3,
        start_time=datetime.now(),
        end_time=datetime.now() + timedelta(hours=1),
    )
    session.add_all([team1, team2, team3, team4])


@pytest.fixture
def fake_team_fixture(session: Session):
    def load_fixture():
        create_fake_teams(session)
        session.commit()

    return load_fixture
