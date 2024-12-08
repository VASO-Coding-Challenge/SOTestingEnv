"""File to contain all Team and TeamMember related tests"""

from datetime import datetime
from ..models import Team, TeamMember

from ..services.exceptions import ResourceNotFoundException

import pytest
from .fixtures import team_svc
from .fake_data.team import fake_team_fixture, team1, team2, team3
from .fake_data.team_members import fake_team_members_fixture

# TODO: Test table reading and exporting functions

__authors__ = ["Andrew Lockard"]


def test_get_team_basic(team_svc, fake_team_fixture):
    """Test the getting of an ordinary Team in the database"""
    fake_team_fixture()
    assert team_svc.get_team(1).name == team1.name
    assert team_svc.get_team("B2").id == team2.id


def test_get_team_not_exist(team_svc, fake_team_fixture):
    """Test that getting a team that does not exist results in an Error"""
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team(60)

    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team("H6")


def test_get_team_incorrect(team_svc, fake_team_fixture):
    """Tests that get_team throws error when run with incorrect indentifier"""
    fake_team_fixture()
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


def test_create_team_basic(team_svc, fake_team_fixture):
    """Test the creation of an ordinary Team in the database"""
    fake_team_fixture()
    new_team = Team(
        name="C4",
        start_time=datetime.now(),
        end_time=datetime.now(),
        password="password",
    )
    team_svc.create_team(new_team)
    assert team_svc.get_team("C4").name == new_team.name


def test_get_all_teams_basic(team_svc, fake_team_fixture):
    fake_team_fixture()
    """Test getting all teams in the database"""
    assert len(team_svc.get_all_teams()) == 3


def test_update_team_basic(team_svc, fake_team_fixture):
    """Test updating an ordinary Team in the database"""
    fake_team_fixture()
    team = team_svc.get_team("B1")
    team.name = "A1"
    team_svc.update_team(team)
    assert team_svc.get_team(1).name == "A1"


def test_update_team_not_exist(team_svc, fake_team_fixture):
    """Test updating a team that does not exist results in an Error"""
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        team_svc.update_team(
            Team(
                name="H6",
                start_time=datetime.now(),
                end_time=datetime.now(),
                password="password",
            )
        )


def test_delete_team_basic(team_svc, fake_team_fixture):
    """Test deleting an ordinary Team in the database"""
    fake_team_fixture()
    team_svc.delete_team(team_svc.get_team(1))
    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team(1)


def test_delete_team_not_exist(team_svc, fake_team_fixture):
    """Test deleting a team that does not exist results in an Error"""
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        team_svc.delete_team(
            Team(
                name="H6",
                start_time=datetime.now(),
                end_time=datetime.now(),
                password="password",
            )
        )


def test_delete_all_teams_basic(team_svc, fake_team_fixture):
    """Test deleting all teams in the database"""
    fake_team_fixture()
    team_svc.delete_all_teams()
    assert len(team_svc.get_all_teams()) == 0


def test_add_team_member_basic(team_svc, fake_team_fixture, fake_team_members_fixture):
    """Test adding a team member to a team"""
    fake_team_fixture()
    new_member = TeamMember(first_name="John", last_name="Doe", team_id=1, id=None)
    team_svc.add_team_member(new_member, team_svc.get_team(1))
    assert len(team_svc.get_team(1).members) == 1


def test_delete_team_deletes_team_members(
    team_svc, fake_team_fixture, fake_team_members_fixture
):
    """Test that deleting a team also deletes its team members"""
    fake_team_fixture()
    team_svc.delete_team(1)
    with pytest.raises(ResourceNotFoundException):
        team_svc.get_team_member(1, 1)
