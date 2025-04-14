"""File to contain all Session_Obj related tests"""

from datetime import datetime
from sqlmodel import select
from backend.models import Session_Obj, Team
from .fixtures import session_obj_svc
from backend.test.fake_data.session_obj import fake_session_fixture
from backend.test.fake_data.team import fake_team_fixture
import pytest

from backend.services.exceptions import (
    ResourceNotAllowedException,
    ResourceNotFoundException,
)

__authors__ = ["Michelle Nguyen," "Tsering Lama"]


def test_get_session(session_obj_svc, fake_session_fixture, fake_team_fixture):
    """Test the getting of an ordinary Session in the database"""
    fake_session_fixture()
    fake_team_fixture()
    assert session_obj_svc.get_session_obj(1).name == "Session 1"
    assert len(session_obj_svc.get_session_obj(1).teams) == 1


def test_get_session_not_exist(session_obj_svc, fake_session_fixture):
    """Test that getting a session that does not exist results in an Error"""
    fake_session_fixture()
    with pytest.raises(ResourceNotFoundException):
        session_obj_svc.get_session_obj(52)


def test_get_all_sessions(session_obj_svc, fake_session_fixture):
    """Test getting all sessions in the database"""
    fake_session_fixture()
    sessions = session_obj_svc.get_all_session_objs()
    assert len(sessions) == 4


def test_create_session(session_obj_svc, fake_session_fixture):
    """Test creating a session"""
    fake_session_fixture()
    new_session = Session_Obj(
        name="Test Create Session",
        start_time=datetime.now(),
        end_time=datetime.now(),
        id=100,
        team_ids=[],
    )
    created_session = session_obj_svc.create_session_obj(new_session)
    assert (
        session_obj_svc.get_session_obj(created_session.id).name
        == "Test Create Session"
    )


def test_update_session(session_obj_svc, fake_session_fixture):
    """Test updating an ordinary Session in the database"""
    fake_session_fixture()
    session = session_obj_svc.get_session_obj(1)
    update_data = Session_Obj(
        name="Test Update Session 1",
        start_time=session.start_time,
        end_time=session.end_time,
        teams=[team.id for team in session.teams],  # ??
    )
    session_obj_svc.update_session_obj(1, update_data)
    assert session_obj_svc.get_session_obj(1).name == "Test Update Session 1"


def test_update_session_not_exist(session_obj_svc, fake_session_fixture):
    """Test updating a session that does not exist results in an Error"""
    fake_session_fixture()

    update_data = Session_Obj(
        name="Updated Session 52",
        start_time=datetime.now(),
        end_time=datetime.now(),
        team_ids=[],
    )
    with pytest.raises(ResourceNotFoundException):
        session_obj_svc.update_session_obj(52, update_data)


def test_delete_session(session_obj_svc, fake_session_fixture):
    """Test deleting an ordinary Session in the database"""
    fake_session_fixture()
    session_obj_svc.delete_session_obj(1)
    with pytest.raises(ResourceNotFoundException):
        session_obj_svc.get_session_obj(1)


def test_delete_session_not_exist(session_obj_svc, fake_session_fixture):
    """Test deleting a team that does not exist results in an Error"""
    fake_session_fixture()
    assert session_obj_svc.delete_session_obj(52) == False


def test_delete_all_session(session_obj_svc, fake_session_fixture):
    """Test deleting all teams in the database"""
    fake_session_fixture()
    session_obj_svc.delete_all_session_objs()
    assert len(session_obj_svc.get_all_session_objs()) == 0


def test_add_teams_one(session_obj_svc, fake_session_fixture, fake_team_fixture):
    """Test adding one Team to a Session"""
    fake_session_fixture()
    fake_team_fixture()
    original_session = session_obj_svc.get_session_obj(2)
    original_len = len(original_session.teams)
    session_obj_svc.add_teams_to_session(2, [3])
    updated_session = session_obj_svc.get_session_obj(2)
    assert len(updated_session.teams) == original_len + 1


def test_add_teams_many(session_obj_svc, fake_session_fixture, fake_team_fixture):
    """Test adding multiple Teams to a Session"""
    fake_session_fixture()
    fake_team_fixture()
    teams_to_modify = session_obj_svc._session.exec(
        select(Team).where(Team.id.in_([3, 4]))
    ).all()

    for team in teams_to_modify:
        team.session_id = None
        
    session_obj_svc._session.commit()
    original_session = session_obj_svc.get_session_obj(2)
    original_len = len(original_session.teams)
    session_obj_svc.add_teams_to_session(2, [3, 4])
    updated_session = session_obj_svc.get_session_obj(2)
    assert len(updated_session.teams) == original_len + 2


def test_add_teams_already_exist(
    session_obj_svc, fake_session_fixture, fake_team_fixture
):
    """Test adding teams that already have a session results in an Error"""
    fake_session_fixture()
    fake_team_fixture()
    with pytest.raises(ResourceNotAllowedException):
        session_obj_svc.add_teams_to_session(1, [2])


def test_add_teams_not_exist(session_obj_svc, fake_session_fixture, fake_team_fixture):
    """Test adding a team that does not exist results in an Error"""
    fake_session_fixture()
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        session_obj_svc.add_teams_to_session(3, [52])


def test_remove_teams_one(session_obj_svc, fake_session_fixture, fake_team_fixture):
    """Test removing multiple Teams from a Session"""
    fake_session_fixture()
    fake_team_fixture()

    session = session_obj_svc.get_session_obj(1)
    old_num = len(session.teams)

    assert old_num > 0
    team_id_to_remove = session.teams[0]

    session_obj_svc.remove_teams_from_session(1, [team_id_to_remove])

    updated_session = session_obj_svc.get_session_obj(1)
    assert len(updated_session.teams) == old_num - 1


def test_remove_teams_many(session_obj_svc, fake_session_fixture, fake_team_fixture):
    fake_session_fixture()
    fake_team_fixture()
    
    team_id = 3  
    session_obj_svc.add_teams_to_session(1, [team_id])
    
    session = session_obj_svc.get_session_obj(1)
    old_num = len(session.teams)
    
    assert old_num >= 2
    team_ids_to_remove = session.teams[:2]
    
    session_obj_svc.remove_teams_from_session(1, team_ids_to_remove)
    
    updated_session = session_obj_svc.get_session_obj(1)
    assert len(updated_session.teams) == old_num - 2


def test_remove_teams_not_exist(
    session_obj_svc, fake_session_fixture, fake_team_fixture
):
    """Test removing a Team that does not exist results in an Error"""
    fake_session_fixture()
    fake_team_fixture()
    with pytest.raises(ResourceNotFoundException):
        session_obj_svc.remove_teams_from_session(1, [999])
