"""Test configuration file for pytest, sets up database fixtures"""

import pytest
import os

from sqlmodel import create_engine, Session, SQLModel

SQLITE_DATABASE_NAME = "test_database.db"
SQLITE_DATABASE_URL = (
    f"sqlite:////workspaces/SOTestingEnv/backend/test/{SQLITE_DATABASE_NAME}"
)

__authors__ = ["Andrew Lockard"]


@pytest.fixture(scope="session")
def test_engine():
    return create_engine(SQLITE_DATABASE_URL)


@pytest.fixture(scope="function")
def session(test_engine):
    """Resets database tables and return a new session object"""
    SQLModel.metadata.drop_all(test_engine)
    SQLModel.metadata.create_all(test_engine)
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()
