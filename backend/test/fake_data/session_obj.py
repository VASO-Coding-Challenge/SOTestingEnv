from sqlmodel import Session, select
from datetime import datetime, timedelta
from backend.db import db_session
from backend.models.session_obj import Session_Obj as SessionModel
import pytest
from backend.db import engine

from backend.models.team import Team

__authors__ = ["Ivan Wu", "Michelle Nguyen"]


def create_fake_sessions(session: Session):
    """Create fake sessions for testing purposes."""
    session1 = SessionModel(
        id=1,
        name="Session 1",
        start_time=datetime.now() - timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=1),
    )
    session2 = SessionModel(
        id=2,
        name="Session 2",
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=4),
    )
    session3 = SessionModel(
        id=3,
        name="Session 3",
        start_time=datetime.now() + timedelta(hours=1),
        end_time=datetime.now() + timedelta(hours=2),
    )
    session4 = SessionModel(
        id=4,
        name="Session 4",
        start_time=datetime.now() + timedelta(hours=2),
        end_time=datetime.now() + timedelta(hours=2),
    )
    session.add_all([session1, session2, session3, session4])


@pytest.fixture
def fake_session_fixture(db_session: Session):
    def load_fixture():
        create_fake_sessions(db_session)
        db_session.commit()

    return load_fixture
