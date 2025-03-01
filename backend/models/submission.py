"""Model for the Team table that stores official team information"""

from sqlmodel import SQLModel


__authors__ = ["Nicholas Almy"]


class Submission(SQLModel):
    """Model for Submissions"""

    file_contents: str
    question_num: str


class ConsoleLog(SQLModel):
    """Model for Console Logs"""

    console_log: str

class ScoredTest(ConsoleLog):
    """Model to hold a scored test"""

    test_name: str
    question_num: int
    score: float
    max_score: float
