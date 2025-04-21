"""Pytest file containing all service fixtures for easy import into pytest functions"""

import pytest
from unittest.mock import patch
from ..services import (
    AuthService,
    PasswordService,
    QuestionService,
    SubmissionService,
    TeamService,
    Session_ObjService,
    ESService
)

from sqlmodel import Session

__authors__ = ["Andrew Lockard", "Michelle Nguyen," "Tsering Lama"]


@pytest.fixture()
def team_svc(session: Session):
    return TeamService(session)


@pytest.fixture()
def auth_svc(session: Session, team_svc):
    return AuthService(session, team_svc)


@pytest.fixture()
def password_svc(session: Session):
    return PasswordService(session)


@pytest.fixture()
def question_svc():
    # TODO: Need to create mocks to change how sample questions and documentation are loaded
    return QuestionService()


@pytest.fixture()
def submission_svc():
    return SubmissionService()


@pytest.fixture()
def session_obj_svc(session: Session):
    return Session_ObjService(session)


@pytest.fixture
def es_svc():
    return ESService()