"""File to contain all Team and TeamMember related tests"""

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

# TODO: Test table reading and exporting functions

__authors__ = ["Andrew Lockard"]


def test_get_team_basic(team_svc, fake_team_fixture):
    """Test the getting of an ordinary Team in the database"""
    fake_team_fixture()
    assert team_svc.get_team(1).name == "B1"
    assert team_svc.get_team("B2").id == 2


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
    assert team_svc.get_team(4).id == new_team.id


def test_df_to_table_basic(team_svc, fake_team_fixture):
    """Test the creation of an ordinary Team in the database"""
    fake_team_fixture()
    new_team = pl.DataFrame(
        {
            "Team Number": ["C4"],
            "Start Time": [datetime.now().strftime("%m/%d/%Y %H:%M")],
            "End Time": [datetime.now().strftime("%m/%d/%Y %H:%M")],
            "Password": ["password"],
        }
    )
    new_team = team_svc.df_to_teams(new_team)[0]
    assert "C4" == new_team.name


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


def test_get_team_members_with_credentials(team_svc, fake_team_fixture):
    """Test getting team members with credentials"""
    fake_team_fixture()
    team = team_svc.get_team_with_credentials("B1", "a-b-c")
    assert team.name == "B1"


def test_get_team_with_credentials_incorrect(team_svc, fake_team_fixture):
    """Test getting team with incorrect credentials"""
    fake_team_fixture()
    with pytest.raises(InvalidCredentialsException):
        team_svc.get_team_with_credentials("B1", "password")


def test_delete_all_teams_basic(team_svc, fake_team_fixture):
    """Test deleting all teams in the database"""
    fake_team_fixture()
    team_svc.delete_all_teams()
    assert len(team_svc.get_all_teams()) == 0


def test_add_team_member_basic(team_svc, fake_team_fixture, fake_team_members_fixture):
    """Test adding a team member to a team"""
    fake_team_fixture()
    original_len = len(team_svc.get_team(1).members)
    new_member = TeamMember(first_name="John", last_name="Doe", team_id=1, id=None)
    team_svc.add_team_member(new_member, team_svc.get_team(1))
    assert len(team_svc.get_team(1).members) == original_len + 1


def test_delete_team_members(team_svc, fake_team_fixture, fake_team_members_fixture):
    """Test deleting a team member from a team"""
    fake_team_fixture()
    old_num = len(team_svc.get_team(1).members)
    new_member = TeamMember(first_name="John", last_name="Doe", team_id=1, id=None)
    team_svc.add_team_member(new_member, team_svc.get_team(1))
    team_svc.delete_team_member(1, team_svc.get_team(1))
    assert len(team_svc.get_team(1).members) == old_num


def test_delete_team_deletes_team_members(
    team_svc, fake_team_fixture, fake_team_members_fixture, session
):
    """Test that deleting a team also deletes its team members"""
    fake_team_fixture()
    team_svc.delete_team(team_svc.get_team(1))
    assert session.get(TeamMember, 1) is None


def test_df_to_team_val_error(team_svc, fake_team_fixture):
    """Test that a value error is raised when a dataframe is not formatted correctly"""
    fake_team_fixture()
    new_team = pl.DataFrame(
        {
            "Team Number": ["C4"],
            "Start Time": [datetime.now().strftime("%m/%d/%Y %H:%M")],
            "End Time": [datetime.now().strftime("%m/%d/%Y %H:%M")],
            "Password": [4],
        }
    )
    with pytest.raises(ValueError):
        team_svc.df_to_teams(new_team)


def test_df_to_team_type_error(team_svc, fake_team_fixture):
    """Test that a type error is raised when a dataframe is not formatted correctly"""
    fake_team_fixture()
    new_team = pl.DataFrame(
        {
            "Team Number": ["C4"],
            "Start Time": [datetime.now().strftime("%m/%d/%Y %H:%M")],
            "End Time": [datetime.now()],
            "Password": [4],
        }
    )
    with pytest.raises(TypeError):
        team_svc.df_to_teams(new_team)


def test_teams_to_df_basic(team_svc, fake_team_fixture):
    """Test that a list of teams can be converted to a DataFrame"""
    fake_team_fixture()
    teams = team_svc.get_all_teams()
    df = team_svc.teams_to_df(teams)
    assert len(df) == 3
    assert "Team Number" in df.columns
    assert "Password" in df.columns
    assert "Start Time" in df.columns
    assert "End Time" in df.columns


def test_create_team_team_data(team_svc, fake_team_fixture):
    """Test creating a team from TeamData"""
    fake_team_fixture()
    team_data = TeamData(
        name="C4",
        start_time=datetime.now(),
        end_time=datetime.now(),
        password="password",
    )
    team_svc.create_team(team_data)
    assert team_svc.get_team("C4").name == team_data.name


def test_team_member_not_found_deleting(team_svc, fake_team_fixture):
    """Test that a team member is not found if the team does not exist"""
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        team_svc.delete_team_member(100, team_svc.get_team(1))


def test_create_team_team_data(team_svc, fake_team_fixture):
    """Test creating a team from TeamData"""
    fake_team_fixture()
    team_data = TeamData(
        name="C4",
        start_time=datetime.now(),
        end_time=datetime.now(),
        password="password",
    )
    team_svc.create_team(team_data)
    assert team_svc.get_team("C4").name == team_data.name


def test_team_member_not_found_deleting(team_svc, fake_team_fixture):
    """Test that a team member is not found if the team does not exist"""
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        team_svc.delete_team_member(100, team_svc.get_team(1))


def test_team_member_not_allowed_deleting(team_svc, fake_team_fixture):
    """Test that a team member is not found if the team does not exist"""
    fake_team_fixture()
    with pytest.raises(ResourceNotAllowedException):
        team_svc.delete_team_member(
            team_svc.get_team("B2").members[0].id, team_svc.get_team("B1")
        )
