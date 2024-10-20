from typing import Optional
import jwt
from datetime import datetime, timedelta
from fastapi import Depends
from sqlmodel import Session

from backend.db import db_session
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.models.team import Team

__authors__ = ["Mustafa Aljumayli"]


class AuthService:
    """Service that performs authentication and token generation."""

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def verify_password(self, plain_password: str, stored_password: str) -> bool:
        """Verify if the plain password matches the stored password."""
        # Simple string comparison for plain text passwords
        return plain_password == stored_password

    def authenticate_and_generate_token(
        self, name: str, password: str, team: Team
    ) -> Optional[str]:
        """Authenticate user and generate a JWT token."""
        if not team or not self.verify_password(password, team.password):
            return None
        token = self.create_access_token(data={"sub": team.name})
        return token

    def create_access_token(self, data: dict) -> str:
        """Generates a JWT token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
