"""Service to handle the Teams feature"""

from typing import List, Optional

from backend.models.session_obj import Session_Obj
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select, and_, delete
import polars as pl
import datetime as dt
import random
import string

from .exceptions import (
    ResourceNotFoundException,
    InvalidCredentialsException,
    ResourceNotAllowedException,
)

from ..models import Team, TeamData, TeamMember, TeamMemberCreate
from ..models.team import TeamPublic


__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard", "Ivan Wu", "Tsering Lama"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class TeamService:
    """Service that preforms actions on Team Table."""

    def __init__(
        self, 
        session: Session = Depends(db_session),
        pwd_svc = None  # Make PasswordService optional
    ):  
        self._session = session
        # Lazy import to avoid circular import
        if pwd_svc is None:
            from .passwords import PasswordService
            self._pwd_svc = PasswordService(session)
        else:
            self._pwd_svc = pwd_svc

    def df_row_to_team(self, team_df: pl.DataFrame) -> TeamData:
        """Converts a DataFrame row to a Team object.
        Args:
            team_df (pl.DataFrame): DataFrame row to convert
        Returns:
            Team: Team object created from the DataFrame row
        """
        try:
            team = TeamData(
                name=team_df["Team Number"],
                password=team_df["Password"],
                start_time=dt.datetime.strptime(
                    team_df["Start Time"], "%m/%d/%Y %H:%M"
                ),
                end_time=dt.datetime.strptime(team_df["End Time"], "%m/%d/%Y %H:%M"),
                session_id=team_df.get("Session ID"),  # necessary?
            )
        except ValueError:
            raise ValueError(f"ValueError while processing {team_df}")
        except TypeError:
            raise TypeError(f"TypeError while processing {team_df}")
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
                "Session ID": [team.session_id],
                "Start Time": [team.start_time.strftime("%m/%d/%Y %H:%M") if team.start_time else ""],
                "End Time": [team.end_time.strftime("%m/%d/%Y %H:%M") if team.end_time else ""]
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

    def update_team(self, team: TeamData) -> TeamData:
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
            existing_team.session_id = team.session_id  # update session assignment
            self._session.add(existing_team)
            self._session.commit()
            return existing_team
        else:
            raise ResourceNotFoundException("Team", team.name)

    def create_team(self, team: Team | TeamData) -> Team:
        """Create a new team in the database.
        Args:
            team (Team): Team object to create
        Returns:
            Team: Created Team object
        """
        # Check if team name already exists
        if isinstance(team, TeamData):
            name = team.name
        else:
            name = team.name
            
        if self.team_name_exists(name):
            raise ResourceNotAllowedException(f"A team with name '{name}' already exists")

        if isinstance(team, TeamData):
            # Generate a random password if one isn't provided or if it's empty
            password = team.password
            if not password or password.strip() == "" or password == "string":
                password = self._pwd_svc.generate_password()
            
            # Create the team with the password and explicitly set session_id
            team = Team(
                name=team.name,
                password=password,
                start_time=team.start_time,
                end_time=team.end_time,
                session_id=None
            )
        else:
            # If a Team object was provided, use it as is
            pass
                
        self._session.add(team)
        self._session.commit()
        self._session.refresh(team)
        return team

    def create_batch_teams(self, team_names_or_prefix, batch_size_or_template, template=None):
        """Create multiple teams based on a template.
        This method supports two calling patterns:
        1. create_batch_teams(prefix, batch_size, template)
        2. create_batch_teams(team_names, team_template)
        Args:
            team_names_or_prefix: Either a list of team names or a template prefix
            batch_size_or_template: Either the batch size or the team template
            template: Template for team data (only used in first calling pattern)
        Returns:
            List[Team]: List of created teams
        Raises:
            ResourceNotAllowedException: If all requested team names already exist
        """
        # Detect which calling pattern is being used
        if isinstance(team_names_or_prefix, list) and template is None:
            # Second pattern: team_names, team_template
            team_names = team_names_or_prefix
            team_template = batch_size_or_template
            
            created_teams = []
            skipped_names = []
            
            # Base template data
            start_time = team_template.start_time
            end_time = team_template.end_time
            
            for team_name in team_names:
                # Check if this specific name already exists
                if self.team_name_exists(team_name):
                    skipped_names.append(team_name)
                    continue
                
                # Generate password using PasswordService
                password = self._pwd_svc.generate_password()
                
                # Create new team
                new_team = Team(
                    name=team_name,
                    password=password,
                    start_time=start_time,
                    end_time=end_time,
                    session_id=None
                )
                
                self._session.add(new_team)
                created_teams.append(new_team)
                
            # If all teams were skipped, raise an exception
            if len(skipped_names) == len(team_names):
                raise ResourceNotAllowedException(
                    f"All requested team names already exist: {', '.join(skipped_names)}"
                )
            
        else:
            # First pattern: template_name, batch_size, template
            template_name = team_names_or_prefix
            batch_size = batch_size_or_template
            
            created_teams = []
            skipped_names = []
            
            # Base template data
            start_time = template.start_time
            end_time = template.end_time
            
            # Find the highest existing number for this prefix
            existing_teams = self._session.exec(
                select(Team).where(Team.name.like(f"{template_name}%"))
            ).all()
            
            # Track highest existing number
            highest_num = 0
            for team in existing_teams:
                # Extract number from team name (e.g., "B1" -> 1)
                try:
                    name_parts = team.name.split(template_name)
                    if len(name_parts) > 1 and name_parts[1].isdigit():
                        num = int(name_parts[1])
                        highest_num = max(highest_num, num)
                except (ValueError, IndexError):
                    continue
            
            # Create new teams starting from the next available number
            teams_to_create = batch_size
            attempts = 0
            max_attempts = batch_size * 2  # Avoid infinite loop
            
            while teams_to_create > 0 and attempts < max_attempts:
                attempts += 1
                team_name = f"{template_name}{highest_num + attempts}"
                
                # Skip if this specific name already exists
                if self.team_name_exists(team_name):
                    skipped_names.append(team_name)
                    continue
                
                # Generate password using PasswordService
                password = self._pwd_svc.generate_password()
                
                # Create new team
                new_team = Team(
                    name=team_name,
                    password=password,
                    start_time=start_time,
                    end_time=end_time,
                    session_id=None
                )
                
                self._session.add(new_team)
                created_teams.append(new_team)
                teams_to_create -= 1
                
            # If no teams were created, raise an exception
            if not created_teams:
                if skipped_names:
                    message = f"Could not create any teams. The following names already exist: {', '.join(skipped_names[:10])}"
                    if len(skipped_names) > 10:
                        message += f" and {len(skipped_names) - 10} more."
                else:
                    message = "Could not create any teams due to naming conflicts."
                raise ResourceNotAllowedException(message)
        
        # Only commit if we're actually creating teams
        if created_teams:
            self._session.commit()
            
            # Refresh all teams to get their IDs
            for team in created_teams:
                self._session.refresh(team)
                
        return created_teams

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
        """Gets a list of all the teams
        
        Returns:
            List[Team]: List of all teams
        """
        teams = self._session.exec(select(Team)).all()
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
        """Deletes all teams and their members
        
        Returns:
            bool: True if operation successful
        """
        # First delete all team members
        self._session.exec(delete(TeamMember))
        # Then delete all teams
        self._session.exec(delete(Team))
        self._session.commit()
        return True
    
    def delete_team_by_id(self, team_id: int) -> bool:
        """Deletes a team by its ID
        
        Args:
            team_id (int): ID of the team to delete
            
        Returns:
            bool: True if team was deleted, False if team wasn't found
            
        Note: This will also delete all associated team members
        """
        # Find the team
        team = self._session.get(Team, team_id)
        if not team:
            return False
            
        # Delete all members of this team
        self._session.exec(delete(TeamMember).where(TeamMember.team_id == team_id))
        
        # Delete the team
        self._session.delete(team)
        self._session.commit()
        return True

    def delete_team(self, team: TeamData | Team) -> bool:
        """Deletes a team"""
        team = self.get_team(team.name)
        
        # First delete team members
        for member in team.members:
            self._session.delete(member)
        
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
        print("Hey")
        member = self._session.get(TeamMember, member_id)
        print("Hey")
        if member == None:
            raise ResourceNotFoundException(f"Member of id={member_id} not found!")

        if member.team_id != team.id:
            raise ResourceNotAllowedException(
                "You must be logged in as the team that the member is a part of to remove that team!"
            )
        self._session.delete(member)
        self._session.commit()

    def get_team_session(self, team_id: int) -> Session_Obj | None:
        """Get the session a team belongs to.

        Args:
            team_id (int): ID of the team
        Returns:
            Session_Obj | None: The session the team belongs to, or None
        Raises:
            ResourceNotFoundException: If team not found
        """
        team = self._session.get(Team, team_id)
        if not team:
            raise ResourceNotFoundException("Team", team_id)
        return team.session
    
    def team_name_exists(self, name: str) -> bool:
        """Check if a team with the given name already exists.
        
        Args:
            name (str): The team name to check
            
        Returns:
            bool: True if the name exists, False otherwise
        """
        existing_team = self._session.exec(
            select(Team).where(Team.name == name)
        ).first()
        return existing_team is not None