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


def teams_to_db():
    args = parse_cli()
    file = args.file
    # Get filepath from cli args, validate it
    if not file.endswith(".csv"):
        sys.stdout.write("Error -- File not in supported format (.csv)")
        sys.stdout.write(f"...Reading from {DEFAULT_FILE}\n")
        file = DEFAULT_FILE

    # Read teams table

    try:
        team_table = pl.read_csv(file)

    except FileNotFoundError:
        sys.stdout.write(f"Error -- File not found...")
        return

    with Session(engine) as session:
        team_svc = TeamService(session)
        pwd_svc = PasswordService(session)
        try:
            team_list = team_svc.df_to_teams(team_table)
        except ValueError:
            sys.stdout.write(
                "Error -- Invalid data in file... Make sure all data entries are valid"
            )
            return

        team_list: list[TeamData] = pwd_svc.generate_passwords(
            teamList=team_list, team_svc=team_svc
        )
        # Delete teams not in the file
        all_teams = team_svc.get_all_teams()
        for db_team in all_teams:
            present = False
            for target_team in team_list:
                if db_team.name == target_team.name:
                    present = True
                    break
            if not present:
                team_svc.delete_team(db_team)

        for team in team_list:
            # Update teams or create them if they do not exist
            try:
                team_svc.update_team(team)
            except ResourceNotFoundException as e:
                team = team_svc.create_team(team)

        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Updates the teams table in the database to match the teams.csv file provided.\n"
        "This command is **NOT safe**... meaning any changes and deletions in the teams.csv will be perminant!",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=DEFAULT_FILE,
        help="File containing updated team information. Upon completing, this database is altered to show the current state of the CSV File.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    teams_to_db()
