"""File to contain all Password Service related tests"""

import pytest
from sqlmodel import select
from backend.models import Word
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