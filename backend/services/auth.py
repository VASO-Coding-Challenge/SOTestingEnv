import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.orm import joinedload
from sqlmodel import select
from ..db import db_session

from ..models.auth import Token, TokenData
from ..models.team import Team

from ..config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES

from .team import TeamService
from .es import ESService
from .exceptions import (
    InvalidCredentialsException,
    ResourceNotFoundException,
    ResourceNotAllowedException,
)

__authors__ = [
    "Mustafa Aljumayli",
    "Andrew Lockard",
    "Nicholas Almy",
    "Nicholas Boyer",
    "Ivan Wu",
]


class AuthService:
    """Service that handles authentication and JWT token generation."""

    def __init__(
        self,
        session: Session = Depends(db_session),
        team_svc: TeamService = Depends(),
        es_svc: ESService = Depends(),
    ):
        self._session = session
        self._team_svc = team_svc
        self._es_svc = es_svc

    def authenticate_team(self, name: str, password: str) -> Token:
        """
        Authenticate the team by checking if the team exists with the given credentials.
        If valid, encode the JWT with token data and return that JWT token.
        """
        try:
            team = self._team_svc.get_team_with_credentials(name, password)
        except InvalidCredentialsException as e:
            raise e

        self._session.add(team)
        self._session.commit()

        # Create TokenData to be encoded
        token_data = TokenData(
            id=team.id,
            name=team.name,
            exp=(
                datetime.now(tz=timezone.utc)
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ),
            is_admin=False,
        )
        print(token_data.model_dump())

        access_token = jwt.encode(
            token_data.model_dump(), SECRET_KEY, algorithm="HS256"
        )

        return Token(access_token=access_token, token_type="bearer")

    def authenticate_es(self, name: str, password: str) -> Token:
        """
        Authenticate the event supervisor by checking if the es exists with the given credentials.
        If valid, encode the JWT with token data and return that JWT token.
        """
        try:
            es = self._es_svc.get_es_with_credentials(name, password)
        except InvalidCredentialsException as e:
            raise e

        # Create TokenData to be encoded
        token_data = TokenData(
            id=1,
            name=es.name,
            exp=(
                datetime.now(tz=timezone.utc)
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ),
            is_admin=True,
        )
        print(token_data.model_dump())

        access_token = jwt.encode(
            token_data.model_dump(), SECRET_KEY, algorithm="HS256"
        )

        return Token(access_token=access_token, token_type="bearer")

    def decode_token(self, token: str) -> TokenData:
        """Given a token, this function will return the TokenData which was encoded."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Validate and extract fields from payload
            return TokenData(**payload)

        except jwt.ExpiredSignatureError:
            raise InvalidCredentialsException(
                "Your JWT Token expired, please log in again."
            )
        except jwt.InvalidTokenError:
            raise InvalidCredentialsException(
                "Your JWT token is invalid. Please log in again."
            )

    def get_team_from_token(self, token: str) -> Team:
        """Gets a team from the users JWT token

        Args:
            token: str - the token sent by the browser
        Returns:
            Team: SQLModel object representing the current logged in team
        Throws:
            InvalidCredientialsException: if JWT did not pass decoding
        """
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            statement = (
                select(Team)
                .options(joinedload(Team.session))
                .where(Team.id == data["id"])
            )
            team = self._session.exec(statement).first()
            if team == None:
                raise ResourceNotFoundException("Team assocated with login not found.")
            return team
        except jwt.ExpiredSignatureError:
            raise InvalidCredentialsException("Login expired, try logging in again.")
        except jwt.InvalidTokenError:
            raise InvalidCredentialsException("Login invalid, try logging in again.")

    def authenticate_team_time(self, team: Team) -> None:
        """Authenticates a Teams permissions based on the time."""
        if team.session.start_time > datetime.now():
            raise ResourceNotAllowedException("Your testing time is not active yet.")
        elif team.session.end_time < datetime.now():
            raise ResourceNotAllowedException("You have run out of time.")
