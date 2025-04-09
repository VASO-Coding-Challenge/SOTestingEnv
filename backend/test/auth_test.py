from datetime import datetime, timedelta, timezone
import pytest
import jwt
from backend.models.team import Team
from backend.services.exceptions import (
    InvalidCredentialsException,
    ResourceNotAllowedException,
    ResourceNotFoundException,
)
from backend.models.auth import TokenData
from sqlmodel import Session
from .fixtures import auth_svc, team_svc
from .fake_data.auth import create_good_teams
from backend.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

__authors__ = ["Michelle Nguyen"]


def test_authenticate_team_success(auth_svc, create_good_teams):
    """Tests a successful authentication"""
    session = create_good_teams
    team = session.get(Team, 1)
    token = auth_svc.authenticate_team(team.name, team.password)
    assert token.token_type == "bearer"
    assert token.access_token is not None

    decoded_token = jwt.decode(token.access_token, key=SECRET_KEY, algorithms=["HS256"])
    assert decoded_token["id"] == team.id
    assert decoded_token["name"] == team.name


def test_authenticate_team_invalid_team(auth_svc):
    """Tests if a team tries to authenticate with an invalid team."""
    with pytest.raises(
        InvalidCredentialsException,
        match="Incorrect credentials. Please try again",
    ):
        auth_svc.authenticate_team(name="nonexistent_team", password="random_password")


def test_authenticate_team_invalid_password(auth_svc, create_good_teams):
    """Tests if a team tries to authenticate with the wrong password."""
    session = create_good_teams
    team = session.get(Team, 2)
    with pytest.raises(InvalidCredentialsException):
        auth_svc.authenticate_team(team.name, "MADEUP_PASSWORD")


def test_authenticate_team_invalid_team_name(auth_svc, create_good_teams):
    """Tests if a team tries to authenticate with the wrong team name."""
    session = create_good_teams
    team = session.get(Team, 2)
    with pytest.raises(InvalidCredentialsException):
        auth_svc.authenticate_team("wrong-name", team.password)


def test_decode_token_success(auth_svc, create_good_teams):
    """Tests a successful token decode from the Authentication Service method."""
    session = create_good_teams
    team = session.get(Team, 1)
    token = auth_svc.authenticate_team(team.name, team.password)

    decoded_token = auth_svc.decode_token(token=token.access_token)
    assert decoded_token.id == team.id
    assert decoded_token.name == team.name


def test_decode_expired_token(auth_svc, create_good_teams):
    """Tests an attempt to decode an expired token."""
    session = create_good_teams
    team = session.get(Team, 2)
    expired_token_data = TokenData(
        id=team.id,
        name=team.name,
        exp=(datetime.now(tz=timezone.utc) - timedelta(hours=1)).timestamp(),
    )

    token = jwt.encode(expired_token_data.model_dump(), SECRET_KEY, algorithm="HS256")

    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc.decode_token(token)
    assert str(exc_msg.value) == "Your JWT Token expired, please log in again."


def test_decode_invalid_token(auth_svc):
    """Tests an attempt to decode an invalid token."""
    token = "MADE_UP_TOKEN"

    with pytest.raises(InvalidCredentialsException) as exc_msg:
        auth_svc.decode_token(token=token)
    assert str(exc_msg.value) == "Your JWT token is invalid. Please log in again."


def test_get_team_from_token_success(auth_svc, create_good_teams):
    """Tests a successful attempt to get a team from a token."""
    session = create_good_teams
    team = session.get(Team, 1)
    token_data = TokenData(
        id=team.id,
        name=team.name,
        exp=(
            datetime.now(tz=timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp(),
    )

    token = jwt.encode(
        payload=token_data.model_dump(), key=SECRET_KEY, algorithm="HS256"
    )

    retrieved_team = auth_svc.get_team_from_token(token=token)

    assert retrieved_team is not None
    assert retrieved_team.id == team.id
    assert retrieved_team.name == team.name


def test_get_team_from_token_expired(auth_svc, create_good_teams):
    """Tests an attempt to use an expired token to get a team."""
    session = create_good_teams
    team = session.get(Team, 1)  # Valid team
    expired_token_data = TokenData(
        id=team.id,
        name=team.name,
        exp=(datetime.now(tz=timezone.utc) - timedelta(hours=1)).timestamp(),
    )

    token = jwt.encode(
        payload=expired_token_data.model_dump(), key=SECRET_KEY, algorithm="HS256"
    )

    with pytest.raises(InvalidCredentialsException, match="Login expired"):
        auth_svc.get_team_from_token(token=token)


def test_get_team_from_token_invalid(auth_svc):
    """Tests an attempt to use an invalid token to get a team."""
    invalid_token = "INVALID.TOKEN.CONTENT"

    with pytest.raises(InvalidCredentialsException, match="Login invalid"):
        auth_svc.get_team_from_token(token=invalid_token)


def test_get_team_from_token_team_not_found(auth_svc, create_good_teams):
    """Tests an attempt to get a team from a token when the team doesn't exist."""
    token_data = TokenData(
        id=999,  # Nonexistent team ID
        name="nonexistent_team",
        exp=(
            datetime.now(tz=timezone.utc)
            + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        ).timestamp(),
    )

    token = jwt.encode(
        payload=token_data.model_dump(), key=SECRET_KEY, algorithm="HS256"
    )

    with pytest.raises(
        ResourceNotFoundException, match="Team assocated with login not found"
    ):
        auth_svc.get_team_from_token(token=token)


def test_authenticate_team_time_before_start(auth_svc, create_good_teams):
    """Tests team authentication fails when the start time is in the future."""
    session = create_good_teams
    team = session.get(Team, 1)

    team.session.start_time = datetime.now() + timedelta(minutes=5)  # Future start
    session.add(team.session)
    session.commit()

    with pytest.raises(
        ResourceNotAllowedException, match="Your testing time is not active yet"
    ):
        auth_svc.authenticate_team_time(team)


def test_authenticate_team_time_after_end(auth_svc, create_good_teams):
    """Tests team authentication fails when the end time has passed."""
    session = create_good_teams
    team = session.get(Team, 1)

    team.session.end_time = datetime.now() - timedelta(minutes=5)  # Past end
    session.add(team.session)
    session.commit()

    with pytest.raises(ResourceNotAllowedException, match="You have run out of time"):
        auth_svc.authenticate_team_time(team)


def test_authenticate_team_time_valid(auth_svc, create_good_teams):
    """Tests successful team authentication within valid time bounds."""
    session = create_good_teams
    team = session.get(Team, 1)
    team.start_time = datetime.now() - timedelta(minutes=30)  # Start time in the past
    team.end_time = datetime.now() + timedelta(minutes=30)  # End time in the future

    # No exception should be raised
    auth_svc.authenticate_team_time(team)
