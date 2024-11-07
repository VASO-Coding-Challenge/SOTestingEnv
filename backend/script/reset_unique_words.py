"""Script to reset the unique words list for password generation"""

from ..services import PasswordService
from sqlmodel import Session
from ..db import engine
import argparse

__authors__ = ["Andrew Lockard", "Nicholas Almy"]


parser = argparse.ArgumentParser(
    description="Reset Unique Word List: This script resets the unique words list for password generation",
).parse_args()

with Session(engine) as session:
    pwd_svc = PasswordService(session)
    pwd_svc.reset_word_list()
    session.commit()
print("Unique words list reset!")
