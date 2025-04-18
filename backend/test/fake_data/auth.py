import pytest
from datetime import datetime, timedelta

from sqlmodel import Session
from backend.models.team import Team
from backend.models import Session_Obj

__authors__ = ["Michelle Nguyen"]


@pytest.fixture
def create_good_teams(session: Session):
    dummy_session = Session_Obj(
        id=1,
        name="Dummy Session",
        start_time=datetime.now() - timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=1),
    )
    session.add(dummy_session)

    team_auth_success = Team(
        id=1,
        name="success",
        password="a-b-c",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() + timedelta(minutes=30),
        session_id=1,
    )

    team_auth_fail = Team(
        id=2,
        name="fail",
        password="fail",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() - timedelta(minutes=5),
        session_id=1,
    )

    session.add_all([team_auth_success, team_auth_fail])
    return session
