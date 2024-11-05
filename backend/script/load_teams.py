import sys
from fastapi import Depends
from sqlmodel import Session
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..models import TeamData
from ..db import engine
import polars as pl
import argparse

__authors__ = ["Nicholas Almy"]

DEFAULT_FILE = "es_files/teams/teams.csv"


def load_teams():
    # Get filepath from cli args, validate it
    args = parse_cli()
    file = args.file
    if not file.endswith(".csv"):
        sys.stdout.write("Error -- File not in supported format (.csv)")
        sys.stdout.write(f"...Reading from {DEFAULT_FILE}")
        file = DEFAULT_FILE

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
                team: TeamData = team_svc.create_team(team)

        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Loads a local teams.csv table into the database. This command will take care of password generation for teams as they are initialized and add them to the csv file. No password overwriting occurs in this script.\n\
            This command is safe... meaning it follows these rules: Where a team is identified by it's team number...\n\
            1)Any team in the database but NOT in the file will be added to the file\n\
            2)Any team in the file but NOT in the database will be added to the database\n\
            3)Any team in both the file and database will update the database to the file's fields (if there are changes)"
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_FILE,
        help="File containing updated team information. Upon completing, this file is altered to show the current state of the team table in the database.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    load_teams()
