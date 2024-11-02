"""Service to handle the Teams feature"""

from typing import List
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select, and_, delete
import polars as pl
import datetime as dt

from .exceptions import (
    ResourceNotFoundException,
    InvalidCredentialsException,
    ResourceNotAllowedException,
)

from ..models import Team, TeamData, TeamMember, TeamMemberCreate

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class TeamService:
    """Service that preforms actions on Team Table."""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    def df_row_to_team(self, team_df: pl.DataFrame) -> TeamData:
        """Converts a DataFrame row to a Team object.
        Args:
            team_df (pl.DataFrame): DataFrame row to convert
        Returns:
            Team: Team object created from the DataFrame row
        """
        team = TeamData(
            name=team_df["Team Number"],
            password=team_df["Password"],
            start_time=dt.datetime.strptime(team_df["Start Time"], "%m/%d/%Y %H:%M"),
            end_time=dt.datetime.strptime(team_df["End Time"], "%m/%d/%Y %H:%M"),
        )
        return team

    def df_to_teams(self, teams_df: pl.DataFrame) -> list[TeamData]:
        """Converts a DataFrame to a list of Team objects.
        Args:
            teams_df (pl.DataFrame): DataFrame to convert
        Returns:
            list[Team]: List of Team objects created from the DataFrame
        """

        teams = []
        for team in teams_df.iter_rows(named="True"):
            teams.append(self.df_row_to_team(team))
        return teams

    def team_to_df(self, team: TeamData) -> pl.DataFrame:
        """Converts a TeamData object to a DataFrame row.
        Args:
            team (TeamData): Team object to convert
        Returns:
            pl.DataFrame: DataFrame row created from the Team object
        """
        team_df = pl.DataFrame(
            {
                "Team Number": [team.name],
                "Password": [team.password],
                "Start Time": [team.start_time.strftime("%m/%d/%Y %H:%M")],
                "End Time": [team.end_time.strftime("%m/%d/%Y %H:%M")],
            }
        )
        return team_df

    def teams_to_df(self, teams: list[TeamData]) -> pl.DataFrame:
        """Converts a list of TeamData objects to a DataFrame.
        Args:
            teams (list[TeamData]): List of Team objects to convert
        Returns:
            pl.DataFrame: DataFrame created from the list of Team objects
        """
        team_dfs = []
        for team in teams:
            team_dfs.append(self.team_to_df(team))
        return pl.concat(team_dfs)

    def team_to_team_data(self, team: Team) -> TeamData:
        """Converts a Team object to a TeamData object.
        Args:
            team (Team): Team object to convert
        Returns:
            TeamData: TeamData object created from the Team object
        """
        team_data = TeamData(
            name=team.name,
            password=team.password,
            start_time=team.start_time,
            end_time=team.end_time,
        )
        return team_data

    def update_team(self, team: TeamData) -> Team:
        """Update a team in the database.
        Args:
            team (Team): Team object to update
        Returns:
            Team: Updated Team object
        Raises:
            ResourceNotFoundException: If the team does not exist in the database
        """
        existing_team: Team | None = self._session.exec(
            select(Team).where(Team.name == team.name)
        ).one_or_none()
        if existing_team:
            existing_team.name = team.name
            existing_team.password = team.password
            existing_team.start_time = team.start_time
            existing_team.end_time = team.end_time
            self._session.add(existing_team)
            self._session.commit()
            return self.team_to_team_data(existing_team)
        else:
            raise ResourceNotFoundException("Team", team.name)

    def create_team(self, team: Team | TeamData) -> Team:
        """Create a new team in the database.
        Args:
            team (Team): Team object to create
        Returns:
            Team: Created Team object
        """
        if isinstance(team, TeamData):
            team = Team(
                name=team.name,
                password=team.password,
                start_time=team.start_time,
                end_time=team.end_time,
            )
        self._session.add(team)
        self._session.commit()
        return team

    def get_team(self, identifier) -> Team:
        """Gets the team by id (int) or name (str)"""
        # TODO: Improve documentation
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

    def delete_all_teams(self):
        """Deletes all teams"""
        self._session.exec(delete(Team))
        self._session.commit()
        return True

    def delete_team(self, team: Team):
        """Deletes a team"""
        self._session.delete(team)
        self._session.commit()
        return True

    def add_team_member(self, new_member: TeamMemberCreate, team: Team) -> TeamMember:
        """Adds a new team member to team: team_id.
        Args:
            team: (Team): Team object of currently logged in user
            new_member (TeamMemberCreate): Data for new member
        Returns:
            TeamMember: The team member object that was added
        """
        member = TeamMember(
            team_id=team.id,
            first_name=new_member.first_name,
            last_name=new_member.last_name,
            id=None,
        )
        self._session.add(member)
        self._session.commit()
        self._session.refresh(member)
        return member

    def delete_team_member(self, member_id: int, team: Team) -> None:
        """Deletes team member with member_id only if they are on team team_id.
        Args:
            member_id (int): team member to delete
            team: (Team): Team object of currently logged in user
        Raises:
            ResourceNotFoundException: If member_id or team_id does not exist
            ResourceNotAllowedException: If team_id does not match the team of the member
        """
        member = self._session.get(TeamMember, member_id)
        if member == None:
            raise ResourceNotFoundException(f"Member of id={member_id} not found!")

        if member.team_id != team.id:
            raise ResourceNotAllowedException(
                "You must be logged in as the team that the member is a part of to remove that team!"
            )
        self._session.delete(member)
        self._session.commit()
