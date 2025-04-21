"""File to contain all Password Service related tests"""

import pytest
from sqlmodel import select
from backend.models import Word
from backend.models.team import Team, TeamData
from backend.services.exceptions import ResourceNotFoundException
from backend.services.passwords import PasswordService
from .fixtures import password_svc

__authors__ = ["Tsering Lama"]


@pytest.fixture
def setup_word_list(session):
    """Setup a list of test words for password generation"""
    words = [
        Word(word="test1", used=False),
        Word(word="test2", used=False),
        Word(word="test3", used=False),
        Word(word="test4", used=False),
        Word(word="test5", used=False),
    ]
    for word in words:
        session.add(word)
    session.commit()
    return words


def test_generate_password(password_svc, setup_word_list):
    """Test password generation creates a proper format"""
    password = password_svc.generate_password()
    
    parts = password.split("-")
    assert len(parts) == 3
    
    for part in parts:
        assert part.strip() != ""


def test_reset_word_list(password_svc, setup_word_list, session):
    """Test that word list is properly reset"""
    words = session.exec(select(Word)).all()
    for word in words[:3]:
        word.used = True
        session.add(word)
    session.commit()
    
    used_words_before = session.exec(select(Word).where(Word.used == True)).all()
    assert len(used_words_before) > 0
    
    password_svc.reset_word_list()
    
    used_words_after = session.exec(select(Word).where(Word.used == True)).all()
    assert len(used_words_after) == 0


def test_generate_password_with_insufficient_words(password_svc, setup_word_list, session, monkeypatch):
    """Test password generation when there are fewer than 3 unused words available"""
    original_reset = PasswordService.reset_word_list
    def mocked_reset(cls=None):
        words = session.exec(select(Word)).all()
        for word in words:
            word.used = False
        session.commit()
    
    PasswordService.reset_word_list = mocked_reset
    
    try:
        words = session.exec(select(Word)).all()
        for word in words[:-2]: 
            word.used = True
            session.add(word)
        session.commit()
        
        unused_words_before = session.exec(select(Word).where(Word.used == False)).all()
        assert len(unused_words_before) < 3
        password = password_svc.generate_password()
        parts = password.split("-")
        assert len(parts) == 3
    finally:
        PasswordService.reset_word_list = original_reset


def test_generate_passwords(password_svc, session, monkeypatch):
    """Test generating passwords for a list of teams with different scenarios"""
    class MockTeamService:
        def get_team(self, name):
            if name == "existing_with_password":
                return Team(name=name, password="existing-password")
            elif name == "existing_no_password":
                return Team(name=name, password=None)
            else:
                raise ResourceNotFoundException(f"Team with name={name} was not found")
    
    password_counter = 0
    def mock_generate_password():
        nonlocal password_counter
        password_counter += 1
        return f"generated-password-{password_counter}"
    
    monkeypatch.setattr(password_svc, "generate_password", mock_generate_password)
    mock_team_svc = MockTeamService()
    teams = [
        TeamData(name="existing_with_password", password="temp", session_id=None),  # Existing team with password in DB
        TeamData(name="existing_no_password", password="temp", session_id=None),    # Existing team without password in DB
        TeamData(name="new_team_no_password", password="temp", session_id=None),    # New team without password
        TeamData(name="new_team_with_password", password="custom-password", session_id=None)  # New team with custom password
    ]

    teams[0].password = None
    teams[1].password = None
    teams[2].password = None
    
    result = password_svc.generate_passwords(teams, mock_team_svc)
    assert result[0].password == "existing-password"  
    assert result[1].password == "generated-password-1" 
    assert result[2].password == "generated-password-2"  
    assert result[3].password == "custom-password"