"""Pytest file containing all service fixtures for easy import into pytest functions"""

import pytest
from ..services import (
    AuthService,
    PasswordService,
    QuestionService,
    SubmissionService,
    TeamService
)
from sqlmodel import Session

@pytest.fixture()
def team_svc(session: Session):
    return TeamService(session)

@pytest.fixture()
def auth_svc(session: Session):
    return AuthService(session)

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