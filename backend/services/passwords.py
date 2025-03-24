"""Service to handle password generation and management"""

from backend.services.exceptions import ResourceNotFoundException
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select
import polars as pl
import datetime as dt
import random


from ..models import TeamData, Team, Word
from .team import TeamService

__authors__ = ["Nicholas Almy", "Andrew Lockard", "Tsering Lama"]


class PasswordService:
    """Service that deals with password generation and management"""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    def generate_passwords(
        self, teamList: list[TeamData], team_svc: TeamService
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
                    team.password = self.generate_password()

            if team.password == None:
                if db_team.password == None:
                    team.password = self.generate_password()
                else:
                    team.password = db_team.password
        return teamList

    def generate_password(self) -> str:
        """Generates and returns a unique 3-word password
        Returns:
            str: The generated password
        """
        corpus = self._session.exec(select(Word).where(Word.used == False)).all()
        if len(corpus) < 3:
            PasswordService.reset_word_list()
            corpus = self._session.exec(select(Word).where(Word.used == False)).all()
        # Randomly select 3 words from the corpus and mark them as used
        password = []
        for _ in range(3):
            word = corpus.pop(random.randint(0, len(corpus) - 1))
            word.used = True
            self._session.add(word)
            self._session.commit()
            password.append(word.word)
        password = "-".join(password)

        return password

    def reset_word_list(self):
        """Resets memory of available password words"""
        words = self._session.exec(select(Word)).all()
        for word in words:
            word.used = False
        self._session.commit()
        return
