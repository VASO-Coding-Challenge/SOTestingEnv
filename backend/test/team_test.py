"""File to contain all Team and TeamMember related tests"""

from datetime import datetime
from ..models import Team, TeamMember

from ..services.exceptions import ResourceNotFoundException

import pytest
from .fake_data.team import fake_team_fixture, team1, team2, team3
from .fake_data.team_members import fake_team_members_fixture

# TODO: Test csv reading and exporting functions

__authors__ = ["Andrew Lockard"]


def test_get_team_basic(team_svc, fake_team_fixture):
    """Test the getting of an ordinary Team in the database"""
    assert team_svc.get_team(1).name == team1.name
    assert team_svc.get_team("B2").id == team2.id


def test_get_team_not_exist(team_svc, fake_team_fixture):
    """Test that getting a team that does not exist results in an Error"""
    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team(60)

    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team("H6")


def test_get_team_incorrect(team_svc, fake_team_fixture):
    """Tests that get_team throws error when run with incorrect indentifier"""
    with pytest.raises(ValueError):
        team_svc.get_team(
            Team(
                name="H7",
                start_time=datetime.now(),
                end_time=datetime.now(),
                id=7,
                password="password",
            )
        )
