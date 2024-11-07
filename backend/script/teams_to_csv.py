import sys
from fastapi import Depends
from sqlmodel import Session
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..models import TeamData
from ..db import engine
import polars as pl
import argparse
from argparse import RawTextHelpFormatter

__authors__ = ["Nicholas Almy"]

DEFAULT_FILE = "es_files/teams/teams.csv"


def teams_to_csv():
    # Get filepath from cli args, validate it
    args = parse_cli()
    file = args.file
    try:
        file: str = sys.argv[1]
        if not file.endswith(".csv"):
            sys.stdout.write("Error -- File not in supported format (.csv)")
            file = DEFAULT_FILE
    except IndexError:
        sys.stdout.write("No file provided")
        file = DEFAULT_FILE

    sys.stdout.write(f"...Writing to {file}")

    with Session(engine) as session:
        team_svc = TeamService(session)
        team_list = team_svc.get_all_teams()
        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Updates or generates a teams.csv file containing the current state of the database.\n"
        "This command is NOT safe... meaning any changes in the teams.csv file will be deleted!",
        formatter_class=RawTextHelpFormatter,
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
    teams_to_csv()
