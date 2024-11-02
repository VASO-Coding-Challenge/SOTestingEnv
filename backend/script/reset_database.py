"""Script to create/reset the SQLite database, add all tables defined in the models package, and insert fake data"""

import os
import polars as pl
from sqlmodel import SQLModel, Session
from ..models import *
from ..db import engine
from ..services.team import TeamService

from ..services import PasswordService

from ..test.fake_data import count, team, word, team_members

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

# * Note this should only be used during development, we will need different scripts for production


# Delete old database if it exists
if os.path.exists("backend/database.db"):
    os.remove("backend/database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    # Add fake data scripts to have them be inserted on database reset
    pwd_svc = PasswordService(session)
    pwd_svc.reset_word_list()
    word.create_words(session)
    count.insert_fake_data(session)
    team.create_fake_teams(session)
    team_svc = TeamService(session)
    team_svc.teams_to_df(team_svc.get_all_teams()).write_csv("es_files/teams.csv")
    team_members.insert_fake_team_members(session)
    session.commit()
