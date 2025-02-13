from sqlmodel import Session
from datetime import datetime, timedelta

import pytest

from backend.models.team import Team
from backend.services.passwords import PasswordService
from backend.db import engine

__authors__ = ["Mustafa Aljumayli", "Nicholas Almy", "Andrew Lockard"]


def create_fake_teams(session: Session):
    """Adds the fake team data for testing purposes with hashed passwords."""
    # Add the teams to the session
    team1 = Team(
        id=1,
        name="B1",
        password="a-b-c",
        session_id=1,
    )
    team2 = Team(
        id=2,
        name="B2",
        password="a-b-c",
        session_id=2,
    )
    team3 = Team(
        id=3,
        name="B3",
        password="a-b-c",
    )
    session.add_all([team1, team2, team3])


@pytest.fixture
def fake_team_fixture(db_session: Session):
    def load_fixture():
        create_fake_teams(db_session)
        db_session.commit()

    return load_fixture
