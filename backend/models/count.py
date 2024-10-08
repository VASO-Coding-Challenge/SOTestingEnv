"""Models for simply testing application setup and demo purposes"""

from sqlmodel import Field, SQLModel

__authors__ = ["Andrew Lockard"]

class Count(SQLModel, table=True): # The table argument here tells SQLModel to implement this as a table
    id: int | None = Field(default=None, primary_key=True) 
    title: str
    count: int = 0 # Sets the default value of count