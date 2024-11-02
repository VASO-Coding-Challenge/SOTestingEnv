import sys
from fastapi import Depends
from sqlmodel import Session
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..models import TeamData
from ..db import engine
import polars as pl


def load_teams():
    # Get filepath from cli args, validate it
    file: str = sys.argv[1]
    if not file.endswith(".csv"):
        sys.stdout.write("Error -- File not in supported format (.csv)")
        sys.stdout.write("...Reading from es_files/teams.csv")
        file = "es_files/teams.csv"

    # Read teams table

    try:
        team_table = pl.read_csv(file)

    except FileNotFoundError:
        sys.stdout.write(
            f"Error -- File not found... generating new table at location {file}"
        )
        team_table = pl.DataFrame(
            {
                "Team Number": [],
                "Password": [],
                "Start Time": [],
                "End Time": [],
            }
        )

    with Session(engine) as session:
        team_svc = TeamService(session)
        pwd_svc = PasswordService(session)
        team_list = team_svc.get_all_teams()
        team_list = team_list + team_svc.df_to_teams(team_table)

        team_list: list[TeamData] = pwd_svc.generate_passwords(
            teamList=team_list, team_svc=team_svc
        )

        for team in team_list:
            # Update teams or create them if they do not exist
            try:
                team_svc.update_team(team)
            except ResourceNotFoundException as e:
                team = team_svc.create_team(team)
                team = team_svc.team_to_team_data(team)

        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


if __name__ == "__main__":
    load_teams()
