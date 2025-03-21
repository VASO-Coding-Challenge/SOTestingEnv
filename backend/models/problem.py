from typing import List
from sqlmodel import SQLModel
from .question import Document


__authors__ = ["Michelle Nguyen"]


class Problem(SQLModel):
    """Model for managing problems."""

    num: int
    prompt: str
    starter_code: str
    test_cases: str
    demo_cases: str
