"""Service to handle the Count example feature"""

from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select
import polars as pl

from .exceptions import ResourceNotFoundException

from ..models import Team

__authors__ = ["Nicholas Almy"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class TeamService:
    """Service that preforms actions on Team Table."""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    # def generate_teams(level: str, number_teams: int, path: str | None):
    #     if path is None:
    #         path = '/workspaces/SOTestingEnv/backend/ES_Files/teams.csv'

    #     user_table = pl.read_csv(path)
    #     if user_table.is_empty():
    #         df = pl.DataFrame({"Team Number": None, "Start Time": None, "End Time": None, "Password": None})
    #     current_user_count = df.

    #     #PATH or DEFAULT_PATH
    #     #If path exists, open file and append new users
    #     #Otherwise, create blank csv

    def generate_team(self, level: str, team_number: int) -> pl.DataFrame:
        team_df = pl.DataFrame(
            {
                "Team Number": f"{level}{team_number}",
                "Start Time": None,
                "End Time": None,
                "Password": self.generate_password(),
            }
        )
        return team_df

    def save_teams_to_csv(self, userTable, path: str):
        """Update User Table with new passwords and users"""
        newUserTable = self.generate_passwords(userTable)
        # TODO -- step to load new users into actual db
        newUserTable.write_csv(path)
        return True

    def generate_passwords(self, userTable: pl.DataFrame) -> pl.DataFrame:
        password_column = userTable["Password"].to_list()
        # Generate new passwords for null entries
        new_passwords = [
            self.generate_password() if p is None else p for p in password_column
        ]
        # Replace the 'password' column with the new passwords
        userTable = userTable.with_columns(pl.Series("Password", new_passwords))
        return userTable

    def generate_password() -> str:
        """Generates and returns a unique 3-word password"""

        corpus = pl.read_csv(WORD_LIST)["word"].shuffle().to_list()
        generated_pwd = f"{corpus.pop()}-{corpus.pop()}-{corpus.pop()}"
        pl.DataFrame({"word": corpus}).write_csv(WORD_LIST)
        return generated_pwd

    def reset_word_list():
        """Resets memory of available password words"""
        pl.read_csv(
            "/workspaces/SOTestingEnv/es_files/unique_words_reset.csv"
        ).write_csv(WORD_LIST)
