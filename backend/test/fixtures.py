"""Pytest file containing all service fixtures for easy import into pytest functions"""

import pytest
from unittest.mock import patch
from ..services import (
    AuthService,
    PasswordService,
    QuestionService,
    SubmissionService,
    TeamService,
)
from backend.test.fake_data.auth import mock_team_service
from sqlmodel import Session

__authors__ = ["Andrew Lockard"]


@pytest.fixture()
def team_svc(session: Session):
    return TeamService(session)


@pytest.fixture()
def auth_svc_with_mock(session, mock_team_service):
    """Provides an AuthService instance with the mocked TeamService."""
    with patch("backend.services.auth.Depends", return_value=mock_team_service):
        yield AuthService(session)


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
