import sys
from fastapi import Depends
from sqlmodel import Session
from ..services.team import TeamService
from ..db import engine
import polars as pl


def main():
    file: str = sys.argv[1]
    if not file.endswith(".csv"):
        sys.stdout.write("Error -- File not in supported format (.csv)")
        return

    user_table = pl.read_csv(file)
    if user_table.is_empty():
        sys.stdout.write("Error -- File not found.")

    with Session(engine) as session:
        team_svc: TeamService = TeamService(session)
        if team_svc.save_and_load_teams(user_table, file):
            sys.stdout.write(f"Saved/updated to file {file}")
        else:
            sys.stdout.write(f"Error -- See logs for more detail")


if __name__ == "__main__":
    main()
