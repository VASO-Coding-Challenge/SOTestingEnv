"""Service to handle password generation and management"""

from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select
import polars as pl
import datetime as dt


from ..models import Team

__authors__ = ["Nicholas Almy"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"


class PasswordService:
    """Service that deals with password generation and management"""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    def generate_passwords(teamList: list[Team]) -> list[Team]:
        """Generates a new password for each user in the list
        Args:
            teamList (list[Team]): List of teams to generate passwords for
        Returns:
            list[Team]: List of teams with updated passwords
        """
        for team in teamList:
            if team.password == None:
                team.password = PasswordService.generate_password()
        return teamList

    def generate_password() -> str:
        """Generates and returns a unique 3-word password
        Returns:
            str: The generated password
        """

        corpus = pl.read_csv(WORD_LIST)["word"].shuffle().to_list()
        generated_pwd = f"{corpus.pop()}-{corpus.pop()}-{corpus.pop()}"
        pl.DataFrame({"word": corpus}).write_csv(WORD_LIST)
        return generated_pwd

    def reset_word_list():
        """Resets memory of available password words"""
        pl.read_csv(
            "/workspaces/SOTestingEnv/es_files/unique_words_reset.csv"
        ).write_csv(WORD_LIST)
