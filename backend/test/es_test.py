"""File to contain all ES related tests"""

import os
import pytest
from unittest import mock
from backend.services.es import ESService, ES
from backend.services.exceptions import InvalidCredentialsException
from .fixtures import es_svc

__authors__ = ["Tsering Lama"]


@pytest.fixture
def mock_env_vars():
    """Fixture to set up mock environment variables for testing"""
    original_env = os.environ.copy()
    os.environ["ES_USERNAME"] = "test_es_user"
    os.environ["ES_PASSWORD"] = "test_es_pass"
    yield
    os.environ = original_env


def test_valid_es_credentials(es_svc, mock_env_vars):
    """Test successful authentication with valid credentials"""
    result = es_svc.get_es_with_credentials("test_es_user", "test_es_pass")
    
    assert isinstance(result, ES)
    assert result.name == "test_es_user"
    assert result.password == "test_es_pass"


def test_invalid_es_credentials(es_svc, mock_env_vars):
    """Test authentication fails with invalid credentials"""
    with pytest.raises(InvalidCredentialsException):
        es_svc.get_es_with_credentials("wrong_username", "wrong_password")


def test_invalid_es_username(es_svc, mock_env_vars):
    """Test authentication fails with valid password but invalid username"""
    with pytest.raises(InvalidCredentialsException):
        es_svc.get_es_with_credentials("wrong_username", "test_es_pass")


def test_invalid_es_password(es_svc, mock_env_vars):
    """Test authentication fails with valid username but invalid password"""
    with pytest.raises(InvalidCredentialsException):
        es_svc.get_es_with_credentials("test_es_user", "wrong_password")