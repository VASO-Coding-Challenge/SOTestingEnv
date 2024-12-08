"""Test configuration file for pytest, sets up database fixtures"""

import pytest
import os

from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool

from .fixtures import *

__authors__ = ["Andrew Lockard"]


@pytest.fixture(scope="function")
def session():
    """Resets database tables and return a new session object"""
    test_engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool, echo=True) # Uses a fully in memory database
    SQLModel.metadata.create_all(test_engine)
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()
