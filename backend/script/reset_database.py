"""Script to create/reset the SQLite database, add all tables defined in the models package, and insert fake data"""

import os
from sqlmodel import SQLModel, Session
from ..models import *
from ..db import engine
from ..services.team import TeamService

from ..test.fake_data import count
from ..test.fake_data import team

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

# * Note this should only be used during development, we will need different scripts for production

TeamService.reset_word_list()

# Delete old database if it exists
if os.path.exists("backend/database.db"):
    os.remove("backend/database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    # Add fake data scripts to have them be inserted on database reset
    count.insert_fake_data(session)
    team.create_fake_teams(session)
    session.commit()
