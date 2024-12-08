import pytest
from datetime import datetime, timedelta

from sqlmodel import Session
from backend.models.team import Team


@pytest.fixture
def create_good_teams(session: Session):
    team_auth_success = Team(
        id=1,
        name="success",
        password="a-b-c",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() + timedelta(minutes=30),
    )

    team_auth_fail = Team(
        id=2,
        name="fail",
        password="fail",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() - timedelta(minutes=5),
    )

    session.add_all([team_auth_success, team_auth_fail])
    return session
