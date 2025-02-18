"""File to contain all session object related tests"""

from datetime import datetime
from backend.models import Team, TeamMember
import polars as pl

from backend.models.team import TeamData
from backend.services.exceptions import (
    InvalidCredentialsException,
    ResourceNotAllowedException,
    ResourceNotFoundException,
)

import pytest
from backend.test.fixtures import team_svc
from backend.test.fake_data.team import fake_team_fixture
from backend.test.fake_data.team_members import fake_team_members_fixture

__authors__ = ["Michelle Nguyen"]


# ```python
# @pytest.fixture()
# def my_svc(session: Session):
#     # Any additional code you need here
#     return MyService(session)
# ```
# > Click [here](https://docs.pytest.org/en/6.2.x/fixture.html#what-fixtures-are) if you would like to learn more about fixtures. Suggested reading is through the section on scope.

# def test_get_team_basic(team_svc, fake_team_fixture):
#     """Test the getting of an ordinary Team in the database"""
#     fake_team_fixture()
#     assert team_svc.get_team(1).name == "B1"
#     assert team_svc.get_team("B2").id == 2


# def test_get_team_not_exist(team_svc, fake_team_fixture):
#     """Test that getting a team that does not exist results in an Error"""
#     fake_team_fixture()
#     with pytest.raises(ResourceNotFoundException):
#         team_svc.get_team(60)

#     with pytest.raises(ResourceNotFoundException):
#         team_svc.get_team("H6")
