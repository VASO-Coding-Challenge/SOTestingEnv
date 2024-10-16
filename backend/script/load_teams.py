import sys
from fastapi import Depends
from sqlmodel import Session
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..models import Team
from ..db import engine
import polars as pl


def main():
    file: str = sys.argv[1]
    if not file.endswith(".csv"):
        sys.stdout.write("Error -- File not in supported format (.csv)")
        return

    team_table = pl.read_csv(file)
    if team_table.is_empty():
        sys.stdout.write("Error -- File not found.")

    with Session(engine) as session:
        team_svc = TeamService(session)

        team_list = team_svc.df_to_teams(team_table)

        team_list: list[Team] = PasswordService.generate_passwords(team_list)

        for team in team_list:
            try:
                print(team)
                team_svc.update_team(team)
            except ResourceNotFoundException as e:
                team_svc.create_team(team)

        team_table = team_svc.teams_to_df(team_list)

    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


if __name__ == "__main__":
    main()
