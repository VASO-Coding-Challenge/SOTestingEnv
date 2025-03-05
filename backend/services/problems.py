"""Service to handle manipulation of problems for ES GUI"""

import os
import shutil

from textwrap import dedent
from typing import List

from fastapi import HTTPException
from ..models import Document, ProblemResponse


__authors__ = ["Michelle Nguyen"]


class ProblemService:
    """Service to handle problem management"""

    QUESTIONS_DIR = "es_files/questions"

    @staticmethod
    def get_problems_list() -> List[int]:
        """Retrieve all available problem numbers."""
        try:
            # Return empty list when no problems exist instead of raising an exception
            if not os.path.exists(ProblemService.QUESTIONS_DIR):
                return []

            problems = sorted(
                [
                    int(f[1:])
                    for f in os.listdir(ProblemService.QUESTIONS_DIR)
                    if f.startswith("q") and f[1:].isdigit()
                ]
            )
            return problems  # Return empty list if no problems found
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error fetching problems: {str(e)}"
            )

    @staticmethod  # I made these methods static because we don't need to store any instance-specific state (self)
    def get_question_path(q_num: int, filename: str) -> str:
        """Get the full file path for a given problem and filename."""
        return os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_num}", filename)

    @staticmethod
    def get_problem(q_num: int) -> ProblemResponse:
        """Retrieve all files related to a problem."""
        if not os.path.exists(os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_num}")):
            raise HTTPException(status_code=404, detail=f"Problem {q_num} not found.")

        try:
            return ProblemResponse(
                num=q_num,
                prompt=ProblemService.read_file(q_num, "prompt.md"),
                starter_code=ProblemService.read_file(q_num, "starter.py"),
                test_cases=ProblemService.read_file(q_num, "test_cases.py"),
                demo_cases=ProblemService.read_file(q_num, "demo_cases.py"),
                docs=ProblemService.load_docs(q_num),
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error retrieving problem {q_num}: {str(e)}"
            )

    @staticmethod
    def read_file(q_num: int, filename: str) -> str:
        """Read content from a specified file in a problem directory."""
        path = ProblemService.get_question_path(q_num, filename)
        if not os.path.exists(path):
            raise HTTPException(
                status_code=404,
                detail=f"File {filename} for problem {q_num} not found.",
            )
        try:
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error reading {filename}: {str(e)}"
            )

    @staticmethod
    def write_file(q_num: int, filename: str, content: str):
        """Write content to a specified file in a problem directory."""
        path = ProblemService.get_question_path(q_num, filename)
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error writing to {filename}: {str(e)}"
            )

    @staticmethod
    def create_problem() -> int:
        """Create a new problem directory with default files."""
        try:
            q_count = 1
            while os.path.exists(
                os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_count}")
            ):
                q_count += 1

            problem_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_count}")
            os.makedirs(problem_path, exist_ok=True)

            # Default content for each file
            default_prompt = "Complete the `first_five` function by returning the first five characters of `string_input`."

            default_starter = dedent(
                """\
            def first_five(string_input: str) -> str:
                # TODO: Fill out this function
                return None
            """
            )

            default_test_cases = dedent(
                """\
            import unittest
            from decorators import weight
            from submission import first_five

            class Test(unittest.TestCase):

                @weight(1)
                def test_first_five1(self):
                    self.assertEqual(first_five("Hello World"), "Hello")
            """
            )

            default_demo_cases = dedent(
                """\
            import unittest
            from submission import first_five

            class Test(unittest.TestCase):

                def test_first_five1(self):
                    self.assertEqual(first_five("Hello World"), "Hello")
            """
            )

            # Write default content to files
            ProblemService.write_file(q_count, "prompt.md", default_prompt)
            ProblemService.write_file(q_count, "starter.py", default_starter)
            ProblemService.write_file(q_count, "test_cases.py", default_test_cases)
            ProblemService.write_file(q_count, "demo_cases.py", default_demo_cases)

            return q_count
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error creating problem: {str(e)}"
            )

    @staticmethod
    def update_problem(
        q_num: int, prompt: str, starter_code: str, test_cases: str, demo_cases: str
    ):
        """Updates all files of a specific problem."""
        problem_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_num}")

        if not os.path.exists(problem_path):
            raise HTTPException(status_code=404, detail=f"Problem {q_num} not found.")

        try:
            ProblemService.write_file(q_num, "prompt.md", prompt)
            ProblemService.write_file(q_num, "starter.py", starter_code)
            ProblemService.write_file(q_num, "test_cases.py", test_cases)
            ProblemService.write_file(q_num, "demo_cases.py", demo_cases)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error updating problem {q_num}: {str(e)}"
            )

    @staticmethod
    def load_docs(q_num: int) -> List[Document]:
        """Load all documentation files for a problem."""
        doc_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_num}")
        if not os.path.exists(doc_path):
            raise HTTPException(status_code=404, detail=f"Problem {q_num} not found.")

        local_docs = []
        try:
            for file in os.listdir(doc_path):
                if file.startswith("doc_") and file.endswith(".md"):
                    doc_title = file[4:-3]  # Extract title from "doc_<title>.md"
                    content = ProblemService.read_file(q_num, file)
                    local_docs.append(Document(content=content, title=doc_title))

            return local_docs
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error loading documentation for problem {q_num}: {str(e)}",
            )

    @staticmethod
    def delete_problem(q_num: int):
        """Deletes a specific problem and renumbers the remaining problems."""
        problem_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{q_num}")

        if not os.path.exists(problem_path):
            raise HTTPException(status_code=404, detail=f"Problem {q_num} not found.")

        try:
            # Remove the specified problem directory
            shutil.rmtree(problem_path)

            # Get remaining problems and sort them
            all_problems = sorted(
                [
                    int(f[1:])
                    for f in os.listdir(ProblemService.QUESTIONS_DIR)
                    if f.startswith("q") and f[1:].isdigit()
                ]
            )

            # Rename problems to maintain consecutive numbering
            for idx, old_q_num in enumerate(all_problems, start=1):
                old_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{old_q_num}")
                new_path = os.path.join(ProblemService.QUESTIONS_DIR, f"q{idx}")

                if old_q_num != idx:  # Rename only if needed
                    shutil.move(old_path, new_path)

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error deleting problem {q_num}: {str(e)}"
            )
