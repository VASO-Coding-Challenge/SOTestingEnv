"""Creates the SQLModel Engine to be used across the application."""

from sqlmodel import create_engine, Session

__authors__ = ["Andrew Lockard"]

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///backend/{sqlite_file_name}"

# TODO: Create script to turn off echo when NOT in development mode
engine = create_engine(sqlite_url, echo=True)


def db_session():
    """Generator function to add dependency injection of SQLModel Sessions"""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
