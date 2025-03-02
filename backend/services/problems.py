"""Service to handle manipulation of problems for ES GUI"""

import os
from typing import List
from ..models import Document, ProblemResponse

__authors__ = ["Michelle Nguyen"]

QUESTIONS_DIR = "es_files/questions"


class ProblemService:
    """Service to handle problem management"""

    @staticmethod  # I made these methods static because we don't need to store any instance-specific state (self)
    def get_question_path(q_num: int, filename: str) -> str:
        """Get the full file path for a given problem and filename."""
        return os.path.join(QUESTIONS_DIR, f"q{q_num}", filename)

    @staticmethod
    def read_file(q_num: int, filename: str) -> str:
        """Read content from a specified file in a problem directory."""
        path = ProblemService.get_question_path(q_num, filename)
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""  # Return empty string if file does not exist

    @staticmethod
    def write_file(q_num: int, filename: str, content: str):
        """Write content to a specified file in a problem directory."""
        path = ProblemService.get_question_path(q_num, filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)

    @staticmethod
    def create_problem() -> int:
        """Create a new problem directory with default files."""
        q_count = 1
        while os.path.exists(os.path.join(QUESTIONS_DIR, f"q{q_count}")):
            q_count += 1

        os.makedirs(os.path.join(QUESTIONS_DIR, f"q{q_count}"), exist_ok=True)

        # Create default files
        ProblemService.write_file(q_count, "prompt.md", "")
        ProblemService.write_file(q_count, "starter.py", "")
        ProblemService.write_file(q_count, "test_cases.py", "")
        ProblemService.write_file(q_count, "demo_cases.py", "")

        return q_count

    @staticmethod
    def get_problem(q_num: int) -> ProblemResponse:
        """Retrieve all files related to a problem."""
        return ProblemResponse(
            num=q_num,
            prompt=ProblemService.read_file(q_num, "prompt.md"),
            starter_code=ProblemService.read_file(q_num, "starter.py"),
            test_cases=ProblemService.read_file(q_num, "test_cases.py"),
            demo_cases=ProblemService.read_file(q_num, "demo_cases.py"),
            docs=ProblemService.load_local_docs(q_num),
        )

    @staticmethod
    def load_local_docs(q_num: int) -> List[Document]:
        """Load all documentation files for a problem."""
        doc_path = os.path.join(QUESTIONS_DIR, f"q{q_num}")
        local_docs = []

        for file in os.listdir(doc_path):
            if file.startswith("doc_") and file.endswith(".md"):
                doc_title = file[4:-3]  # Extract title from "doc_<title>.md"
                content = ProblemService.read_file(q_num, file)
                local_docs.append(Document(content=content, title=doc_title))

        return local_docs
