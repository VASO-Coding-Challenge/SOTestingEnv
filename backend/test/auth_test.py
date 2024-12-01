from datetime import datetime, timedelta, timezone
import pytest
import jwt
from backend.services.exceptions import InvalidCredentialsException
from backend.models.auth import TokenData
from backend.test.fixtures import auth_svc_with_mock
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.test.fake_data.auth import team_auth_success, team_auth_fail

def test_authenticate_team_success(auth_svc_with_mock):
    """Tests a successful authentication."""
    token = auth_svc_with_mock.authenticate_team("success", "a-b-c")
    assert token.token_type == "bearer"
    assert token.access_token is not None

    decoded_token = jwt.decode(token.access_token, key=SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_token["id"] == team_auth_success.id
    assert decoded_token["name"] == team_auth_success.name


def test_authenticate_team_invalid_password(auth_svc_with_mock):
    """Tests if a team tries to authenticate with the wrong password."""
    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc_with_mock.authenticate_team("success", "MADEUP_PASSWORD")
    assert str(exc_msg.value) == "Invalid Credentials. Please check your Name and Password"


def test_authenticate_team_invalid_team_name(auth_svc_with_mock):
    """Tests if a team tries to authenticate with the wrong team name."""
    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc_with_mock.authenticate_team("wrong-name", "a-b-c")
    assert str(exc_msg.value) == "Invalid Credentials. Please check your Name and Password"


def test_decode_token_success(auth_svc_with_mock):
    """Tests a successful token decode from the Authentication Service method."""
    token = auth_svc_with_mock.authenticate_team("success", "a-b-c")

    decoded_token = auth_svc_with_mock.decode_token(token=token.access_token)
    assert decoded_token.id == team_auth_success.id
    assert decoded_token.name == team_auth_success.name


def test_decode_expired_token(auth_svc_with_mock):
    """Tests an attempt to decode an expired token."""
    expired_token_data = TokenData(
        id=team_auth_fail.id,
        name=team_auth_fail.name,
        exp=(datetime.now(tz=timezone.utc) - timedelta(hours=1)).timestamp(),
    )

    token = jwt.encode(expired_token_data.model_dump(), SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc_with_mock.decode_token(token)
    assert str(exc_msg.value) == "Your JWT Token expired, please log in again."


def test_decode_invalid_token(auth_svc_with_mock):
    """Tests an attempt to decode an invalid token."""
    token = "MADE_UP_TOKEN"

    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc_with_mock.decode_token(token=token)
    assert str(exc_msg.value) == "Your JWT token is invalid. Please log in again."


def test_get_team_from_token_success(auth_svc_with_mock):
    """Tests a successful attempt to get a team from a token."""
    token_data = TokenData(
        id=team_auth_success.id,
        name=team_auth_success.name,
        exp=(datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp(),
    )
    token = jwt.encode(
        payload=token_data.model_dump(), key=SECRET_KEY, algorithm=ALGORITHM
    )

    team = auth_svc_with_mock.get_team_from_token(token=token)

    assert team is not None
    assert team.id == team_auth_success.id
    assert team.name == team_auth_success.name
