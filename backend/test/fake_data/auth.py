from unittest.mock import Mock
import pytest
from datetime import datetime, timedelta
from backend.services.team import TeamService
from backend.models.team import Team

# Mock data
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


@pytest.fixture
def mock_team_service():
    """Creates a mock TeamService."""
    mock_service = Mock(spec=TeamService)

    # Mock get_team_with_credentials behavior
    def mock_get_team_with_credentials(name, password):
        if name == "success" and password == "a-b-c":
            return team_auth_success
        elif name == "fail":
            return team_auth_fail
        return None

    mock_service.get_team_with_credentials = Mock(
        side_effect=mock_get_team_with_credentials
    )
    return mock_service
