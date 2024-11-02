import sys
from fastapi import Depends
from sqlmodel import Session
from ..models import TeamData
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..db import engine
import polars as pl
import datetime


def main():
    # Get filepath from cli args, validate it
    prefix: str = sys.argv[1]
    if not prefix.isalpha():
        sys.stdout.write("Error -- Prefix must be alphabetic characters.")
        return

    number_teams: str = sys.argv[2]
    if not number_teams.isdigit():
        sys.stdout.write("Error -- Number of teams must be an integer.")
        return

    date: str = sys.argv[3]
    try:
        datetime.datetime.strptime(date, "%m/%d/%Y")
        print(date)
    except ValueError:
        sys.stdout.write("Error -- Date should be in the format mm/dd/yyyy")
        return

    start_time: str = sys.argv[4]
    try:
        start_time = datetime.datetime.strptime(
            f"{date} {start_time}", "%m/%d/%Y %H:%M"
        )
    except ValueError:
        sys.stdout.write("Error -- Start Time should be in the format HH:MM")
        return

    end_time: str = sys.argv[5]
    try:
        end_time = datetime.datetime.strptime(f"{date} {end_time}", "%m/%d/%Y %H:%M")
    except ValueError:
        sys.stdout.write("Error -- Start Time should be in the format HH:MM")
        return

    file: str = sys.argv[6]
    if not file.endswith(".csv"):
        sys.stdout.write(
            "Error -- File not in supported format (.csv)... setting file to ES_files/teams.csv"
        )
        file = "es_files/teams.csv"

    try:
        team_table = pl.read_csv(file)
    except FileNotFoundError:
        file = "es_files/teams.csv"
        team_table = pl.DataFrame(
            {
                "Team Number": [],
                "Password": [],
                "Start Time": [],
                "End Time": [],
            }
        )
        pass

    with Session(engine) as session:
        team_svc = TeamService(session)
        pwd_svc = PasswordService(session)
        team_list = team_svc.get_all_teams()
        # team_list = team_list + team_svc.df_to_teams(team_table)
        # Find the last team number for the prefix
        last_team = 0
        for team in team_list:
            if team.name.startswith(prefix):
                last_team = max(last_team, int(team.name[len(prefix) :]))
                print(last_team)
        # Create new teams
        for i in range(1, int(number_teams) + 1):
            team = TeamData(
                name=f"{prefix}{last_team + i}",
                password=pwd_svc.generate_password(),
                start_time=start_time,
                end_time=end_time,
            )
            team = team_svc.create_team(team)
            team = team_svc.team_to_team_data(team)
            team_list.append(team)
        # Add new teams to the table
        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(file)

    sys.stdout.write(f"Saved/updated to file {file}")


if __name__ == "__main__":
    main()
