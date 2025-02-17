"""This script adds a specified number and level of teams to the database."""

import sys
from fastapi import Depends
from sqlmodel import Session
from ..models import TeamData
from ..services import TeamService, PasswordService, ResourceNotFoundException
from ..db import engine
import polars as pl
import datetime
import argparse

DEFAULT_FILE = "es_files/teams/teams.csv"


# TODO: Update to use new Team and Session model when implementing functionality to manage teams
def add_teams():
    args = parse_cli()
    if not validate_args(args):
        return

    start_time = datetime.datetime.strptime(
        f"{args.date} {args.start}", "%m/%d/%Y %H:%M"
    )
    end_time = datetime.datetime.strptime(f"{args.date} {args.end}", "%m/%d/%Y %H:%M")

    with Session(engine) as session:
        team_svc = TeamService(session)
        pwd_svc = PasswordService(session)
        team_list = team_svc.get_all_teams()
        # Find the last team number for the prefix
        last_team = 0
        for team in team_list:
            if team.name.startswith(args.prefix):
                last_team = max(last_team, int(team.name[len(args.prefix) :]))
                print(last_team)
        # Create new teams
        for i in range(1, int(args.number) + 1):
            team = TeamData(
                name=f"{args.prefix}{last_team + i}",
                password=pwd_svc.generate_password(),
                start_time=start_time,
                end_time=end_time,
            )
            team: TeamData = team_svc.create_team(team)
            team_list.append(team)
        # Add new teams to the table
        team_table = (
            team_svc.teams_to_df(team_list).unique().sort(["Start Time", "Team Number"])
        )

    # Save the password changes back to file
    team_table.write_csv(args.file)

    sys.stdout.write(f"Saved/updated to file {args.file}")


def parse_cli() -> argparse.Namespace:
    # Get filepath from cli args, validate it
    parser = argparse.ArgumentParser(
        description="This script adds a specified number and level of teams to the database."
    )

    parser.add_argument(
        "prefix",
        type=str,
        help="The prefix for the team name. Must be alphabetic characters.",
    )

    parser.add_argument(
        "number",
        type=int,
        help="The number of teams to create.",
    )

    parser.add_argument(
        "date",
        type=str,
        help="The date of the competition in the format mm/dd/yyyy.",
    )

    parser.add_argument(
        "start",
        type=str,
        help="The start time of the competition in the format HH:MM (24h Time).",
    )

    parser.add_argument(
        "end",
        type=str,
        help="The end time of the competition in the format HH:MM (24h Time).",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="es_files/teams/teams.csv",
        help=f"The file to save the team data to. Defaults to {DEFAULT_FILE}.",
    )
    args = parser.parse_args()
    return args


def validate_args(args: argparse.Namespace) -> bool:
    if not args.prefix.isalpha():
        sys.stdout.write("Error -- Prefix must be alphabetic characters.")
        return False

    if not str(args.number).isdigit():
        sys.stdout.write("Error -- Number of teams must be an integer.")
        return False

    try:
        datetime.datetime.strptime(args.date, "%m/%d/%Y")
    except ValueError:
        sys.stdout.write("Error -- Date should be in the format mm/dd/yyyy")
        return False

    try:
        datetime.datetime.strptime(args.start, "%H:%M")
    except ValueError:
        sys.stdout.write("Error -- Start Time should be in the format HH:MM")
        return False

    try:
        datetime.datetime.strptime(args.end, "%H:%M")
    except ValueError:
        sys.stdout.write("Error -- Start Time should be in the format HH:MM")
        return False

    if not args.file.endswith(".csv"):
        sys.stdout.write(
            f"Error -- File not in supported format (.csv)... setting file to {DEFAULT_FILE}"
        )
        args.file = DEFAULT_FILE

    return True


if __name__ == "__main__":
    add_teams()
