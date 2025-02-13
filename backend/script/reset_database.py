"""Script to create/reset the SQLite database, add all tables defined in the models package, and insert fake data"""

import os
import polars as pl
from sqlmodel import SQLModel, Session
from ..models import *
from ..db import engine
from ..services.team import TeamService

from ..services import PasswordService

from ..test.fake_data import team, word, team_members, session

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

# * Note this should only be used during development, we will need different scripts for production


SQLModel.metadata.drop_all(engine)

SQLModel.metadata.create_all(engine)

with Session(engine) as db_session:
    # Add fake data scripts to have them be inserted on database reset
    pwd_svc = PasswordService(db_session)
    pwd_svc.reset_word_list()
    word.create_words(db_session)
    session.create_fake_sessions(db_session)
    team.create_fake_teams(db_session)
    team_svc = TeamService(db_session)
    team_svc.teams_to_df(team_svc.get_all_teams()).write_csv("es_files/teams/teams.csv")
    team_members.insert_fake_team_members(db_session)
    session.commit()
