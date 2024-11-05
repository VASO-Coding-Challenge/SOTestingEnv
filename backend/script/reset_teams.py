"""Script to reset team table"""

from sqlmodel import Session
from ..services import TeamService
from ..db import engine
import polars as pl

__authors__ = ["Nicholas Almy"]

with Session(engine) as session:
    team_svc = TeamService(session)
    team_svc.delete_all_teams()
    pl.DataFrame(
        {
            "Team Number": [],
            "Password": [],
            "Start Time": [],
            "End Time": [],
        }
    ).write_csv("es_files/teams/teams.csv")
    session.commit()
