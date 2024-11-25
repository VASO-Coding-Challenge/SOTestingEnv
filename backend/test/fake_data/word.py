from sqlmodel import Session
import polars as pl

import pytest

from backend.models.word import Word
from backend.db import engine

__authors__ = ["Nicholas Almy", "Andrew Lockard"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/teams/unique_words_reset.csv"
corpus = pl.read_csv(WORD_LIST)["word"]


def create_words(session: Session):
    """Adds the fake password data for testing purposes with hashed passwords."""
    for word in corpus:
        word = Word(word=word)
        session.add(word)


@pytest.fixture()
def create_words_fixture(session: Session):
    create_words(session)
    session.commit()
