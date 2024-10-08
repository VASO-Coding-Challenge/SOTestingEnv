"""Script to create/reset the SQLite database, add all tables defined in the models package, and insert fake data"""

import os
from sqlmodel import SQLModel, Session
from ..models import *
from ..db import engine

from ..test.fake_data import count

__authors__ = ["Andrew Lockard"]

# * Note this should only be used during development, we will need different scripts for production

# Delete old database if it exists
if os.path.exists("backend/database.db"):
    os.remove("backend/database.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    count.insert_fake_data(session) # Add fake data scripts to have them be inserted on database reset
    session.commit()