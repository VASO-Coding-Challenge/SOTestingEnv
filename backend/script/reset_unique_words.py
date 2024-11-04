"""Script to reset the unique words list for password generation"""

from ..services import PasswordService
from sqlmodel import Session
from ..db import engine

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

with Session(engine) as session:
    pwd_svc = PasswordService(session)
    pwd_svc.reset_word_list()
    session.commit()
print("Unique words list reset!")
