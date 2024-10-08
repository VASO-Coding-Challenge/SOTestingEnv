"""Service to handle the Count example feature"""

from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select

from .exceptions import ResourceNotFoundException

from ..models import Count

__authors__ = ["Andrew Lockard"]

class CountService:
    """Service that preforms actions on the count table"""

    def __init__(self, session: Session = Depends(db_session)): # Add all dependencies via FastAPI injection in the constructor
        self._session = session
    
    def get_counts(self) -> list[Count]:
        """Gets all the current counts"""
        statement = select(Count)
        return self._session.exec(statement).all() # .all() converts the interable returned by .exec into a list of models

    def get_count(self, id: int) -> Count | None:
        """Gets the count with id=id"""
        counter = self._session.get(Count, id)
        if counter == None:
            raise ResourceNotFoundException(f"Counter of id={id} was not found")
        return counter
    
    def add_new_counter(self, new_counter: Count) -> None:
        """Adds a new counter in the shape of the defined Count"""
        new_counter.id = None # Explicitly make sure the id is None so SQLModel can handle the id selection
        self._session.add(new_counter)
        self._session.commit()

    def update_counter(self, id: int, new_count: int) -> Count:
        """Updates a counter's count and returns it"""
        counter = self.get_count(id)
        counter.count = new_count
        self._session.add(counter)
        self._session.commit()
        self._session.refresh(counter) # This line updates the counter in memory to match what is in the database, it's needed after a commit if you intend to use that data in memory later
        return counter
    
    def delete_counter(self, id: int) -> bool:
        """Delets a counter and returns true if it was successful"""
        counter = self.get_count(id)
        self._session.delete(counter)
        self._session.commit()
        return True

