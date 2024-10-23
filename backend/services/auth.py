import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from backend.db import db_session
from backend.models.auth import Token, TokenData, LoginData
from backend.models.team import Team
from backend.config import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.services.team import TeamService
from backend.services.exceptions import InvalidCredentialsException


class AuthService:
    """Service that handles authentication and JWT token generation."""

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def authenticate_team(
        self, name: str, password: str, team_service: TeamService = Depends()
    ) -> Token:
        """
        Authenticate the team by checking if the team exists with the given credentials.
        If valid, encode the JWT with token data and return that JWT token.
        """
        team = team_service.get_team_with_credentials(name, password)
        if not team or team.password != password:
            raise InvalidCredentialsException(
                "Invalid Credentials. Please check your Name and Password"
            )
        team.active_JWT = True
        self._session.add(team)  # Add this to the session
        self._session.commit()

        # Create TokenData, and convert the datetime to an ISO string
        token_data = TokenData(
            id=team.id,
            name=team.name,
            expiration_time=(
                datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            ).isoformat(),  # convert datetime to a string
        )

        # Serialize the token data to a JSON-compatible format
        access_token = jwt.encode(
            token_data.model_dump(), SECRET_KEY, algorithm="HS256"
        )

        return Token(access_token=access_token, token_type="bearer")

    def decode_token(self, token: str) -> TokenData:
        """Given a token, this function will return the TokenData which was encoded."""
        try:
            payload = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
            )

            # Validate and extract fields from payload
            return TokenData(**payload)

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
