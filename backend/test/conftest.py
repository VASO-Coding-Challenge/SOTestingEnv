"""Test configuration file for pytest, sets up database fixtures"""

import pytest
import os

from sqlmodel import create_engine, Session, SQLModel

# SQLITE_DATABASE_NAME = "test_database.db"
# SQLITE_DATABASE_URL = (
#     f"sqlite:////workspaces/SOTestingEnv/backend/test/{SQLITE_DATABASE_NAME}"
# )

# Detect if we're running inside GitHub Actions
if os.getenv("GITHUB_ACTIONS") == "true":
    SQLITE_DATABASE_URL = "sqlite:///test_database.db"
else:
    SQLITE_DATABASE_URL = (
        "sqlite:////workspaces/SOTestingEnv/backend/test/test_database.db"
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
