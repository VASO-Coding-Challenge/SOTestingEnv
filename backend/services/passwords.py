"""Service to handle password generation and management"""

from backend.services.exceptions import ResourceNotFoundException
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select
import polars as pl
import datetime as dt


from ..models import TeamData, Team
from .team import TeamService

__authors__ = ["Nicholas Almy", "Andrew Lockard"]

# TODO: Make this a relative path as I'm unsure if the same file strcture will be retained in the final container
WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"


class PasswordService:
    """Service that deals with password generation and management"""

    def generate_passwords(
        teamList: list[TeamData], team_svc: TeamService
    ) -> list[TeamData]:
        """Generates a new password for each user in the list
        Args:
            teamList (list[Team]): List of teams to generate passwords for
            team_svc (TeamService): Service to interact with the Team table
        Returns:
            list[Team]: List of teams with updated passwords
        """
        for team in teamList:
            try:
                db_team = team_svc.get_team(team.name)
            except ResourceNotFoundException:
                if team.password == None:
                    team.password = PasswordService.generate_password()

            if team.password == None:
                if db_team.password == None:
                    team.password = PasswordService.generate_password()
                else:
                    team.password = db_team.password
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
