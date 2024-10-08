"""Creates Fake Data for the example Count feature"""
from sqlmodel import Session
from ...db import engine # ! Make sure to import the engine, DO NOT create a new one

from ...models.count import Count

__authors__ = ["Andrew Lockard"]

counter1 = Count(title="Assignments Missed")
counter2 = Count(title="Amount of dependencies changed", count=3)
counter3 = Count(title="Water Bottles Consumed Today")

def insert_fake_data(session: Session):
    """Adds the fake data defined above to the session"""
    session.add(counter1)
    session.add(counter2)
    session.add(counter3)
