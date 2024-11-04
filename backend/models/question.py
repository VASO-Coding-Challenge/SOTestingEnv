"""Model for the Team table that stores official team information"""

from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import List


__authors__ = ["Nicholas Almy", "Mustafa Aljumayli", "Andrew Lockard"]


class Document(SQLModel):
    """Model for Documentation"""

    content: str
    title: str


class Question(SQLModel):
    """Question model to store the questions for the competition"""

    num: int
    writeup: str
    docs: List[Document]


class QuestionsPublic(SQLModel):
    """Model to define the API response shape of the Question model"""

    questions: List[Question]
    global_docs: List[Document]
