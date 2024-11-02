"""Script to reset team table"""

from sqlmodel import Session
from ..services import TeamService
from ..db import engine

__authors__ = ["Nicholas Almy"]

with Session(engine) as session:
    team_svc = TeamService(session)
    team_svc.delete_all_teams()
    session.commit()
