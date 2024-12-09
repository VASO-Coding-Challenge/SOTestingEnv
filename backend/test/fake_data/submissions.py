from datetime import datetime, timedelta
import pytest
from sqlmodel import Session
from ...models import Team, Submission

# Mock the send_to_judge0 and package_


@pytest.fixture
def submission_test_data(session: Session):
    team1 = Team(
        id=1,
        name="B1",
        password="a-b-c",
        start_time=datetime.now() - timedelta(minutes=30),
        end_time=datetime.now() + timedelta(minutes=30),
    )

    submission = Submission(
        file_contents="",
    )
