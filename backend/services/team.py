"""Service to handle the Teams feature"""

from typing import List
from sqlalchemy import and_
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select
import polars as pl
import datetime as dt

from .exceptions import ResourceNotFoundException, InvalidCredentialsException

from ..models import Team

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class TeamService:
    """Service that preforms actions on Team Table."""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    def save_and_load_teams(self, userTable, path: str):
        """Update User Table with new passwords and users"""
        newUserTable = self.generate_passwords(userTable)
        # TODO -- step to load new users into actual db
        for user in newUserTable.iter_rows(named="True"):
            # Check if the user already exists in the database by querying based on a unique identifier, e.g., "id"
            existing_user: Team | None = self._session.exec(
                select(Team).where(Team.id == user["id"])
            )

            if existing_user:
                # If the user exists, update the relevant fields
                existing_user.name = user["Team Number"]
                existing_user.password = user["Password"]
                existing_user.start_time = dt.datetime.strptime(
                    user["Start Time"], "%H:%M"
                ).time()
                existing_user.end_time = dt.datetime.strptime(
                    user["End Time"], "%H:%M"
                ).time()
                existing_user.login_time = dt.timedelta(minutes=user["Login Time"])
                existing_user.active_JWT = False
                self._session.add(existing_user)
            else:
                # If the user does not exist, create a new record
                new_user = Team(
                    id=user["id"],
                    name=user["Team Number"],
                    password=self._auth_service.get_password_hash(user["Password"]),
                    start_time=dt.datetime.strptime(user["Start Time"], "%H:%M").time(),
                    end_time=dt.datetime.strptime(user["End Time"], "%H:%M").time(),
                    login_time=dt.timedelta(minutes=user["Login Time"]),
                    disabled=False,
                )
                self._session.add(new_user)

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

    def generate_password(self) -> str:
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

    def get_team(self, identifier) -> Team:
        """Gets the team by id (int) or name (str)"""
        if isinstance(identifier, int):
            team = self._session.get(Team, identifier)
            if team is None:
                raise ResourceNotFoundException(
                    f"Team with id={identifier} was not found"
                )
        elif isinstance(identifier, str):
            team = self._session.exec(
                select(Team).where(Team.name == identifier)
            ).first()
            if not team:
                raise ResourceNotFoundException(
                    f"Team with name={identifier} was not found"
                )
        else:
            raise ValueError("Identifier must be an int (id) or a str (name)")
        return team

    def get_all_teams(self) -> List[Team]:
        """Gets a list of all the teams"""
        teams = self._session.exec(select(Team)).all()
        if not teams:
            raise ResourceNotFoundException(f"Teams were not found")
        return teams

    def get_team_with_credentials(self, name: str, password: str) -> Team:
        """Gets team with a team name and password."""
        team = self._session.exec(
            select(Team).where(and_(Team.name == name, Team.password == password))
        ).first()
        if not team:
            raise InvalidCredentialsException("Incorrect credentials. Please try again")
        return team
