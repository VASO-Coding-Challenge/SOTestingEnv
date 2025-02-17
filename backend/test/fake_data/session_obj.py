from sqlmodel import Session
from datetime import datetime, timedelta
from backend.models.session_obj import Session as SessionModel
import pytest

__authors__ = ["Ivan Wu"]


def create_fake_sessions(db_session: Session):
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
    db_session.add_all([session1, session2])


@pytest.fixture
def fake_session_fixture(db_session: Session):
    def load_fixture():
        create_fake_sessions(db_session)
        db_session.commit()

    return load_fixture
