import sys
from fastapi import Depends
from sqlmodel import Session
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..models import TeamData
from ..db import engine
import polars as pl

__authors__ = ["Nicholas Almy"]

DEFAULT_FILE = "es_files/teams/teams.csv"


def load_teams():
    # Get filepath from cli args, validate it
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


if __name__ == "__main__":
    load_teams()
