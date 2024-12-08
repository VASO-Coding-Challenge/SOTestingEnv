"""Service to handle the Submissions and interaction with Judge0 API"""

import os
import json
import requests  # type: ignore
import base64
from io import BytesIO  # Creates an in-memory "file"
from zipfile import ZipFile

from ..models import Submission, ConsoleLog, Team
from backend.services.exceptions import ResourceNotFoundException

__authors__ = ["Nicholas Almy", "Andrew Lockard"]

submissions_dir = "es_files/submissions"


class SubmissionService:
    """Service that deals with Submission CRUD operations"""

    def __init__(self):
        pass

    def submit(self, team_name: str, submission: Submission) -> None:
        """Submit a file to the submission folder... Only supports Python files"""
        # sys.stdout.write(f"Debug: Team name is {team_name}")
        question_dir = f"q{submission.question_num}"
        file = f"{team_name}.py"

        # Create the submission directory if it doesn't exist
        if not os.path.exists(submissions_dir):
            os.makedirs(submissions_dir)

        # Create the question directory if it doesn't exist
        if not os.path.exists(os.path.join(submissions_dir, question_dir)):
            os.makedirs(os.path.join(submissions_dir, question_dir))

        # Write the file to the submission directory
        with open(os.path.join(submissions_dir, question_dir, file), "w") as f:
            f.write(submission.file_contents)

    def submit_and_run(self, team: Team, submission: Submission) -> ConsoleLog:
        """Submit a file to the submission folder, runs it and returns the console logs"""
        self.submit(team.name, submission)
        return self.run_submission(submission.question_num, team.name, forScore=False)

    def run_submission(
        self, question_num: int, team_name: str, forScore: bool = False
    ) -> ConsoleLog:
        """Run a submission on an Autograder and return the console logs
        Args:
            question_num (int): The question number
            team_name (str): The team name
            forScore (bool): Whether the submission is for final grading or not
        Returns:
            ConsoleLog: The console log of the submission
        """
        submission_zip = self.package_submission(team_name, question_num, not forScore)
        res = requests.post(
            "http://host.docker.internal:2358/submissions?wait=true",
            headers={"Content-Type": "application/json"},
            json={
                "additional_files": submission_zip.decode("utf-8"),
                "language_id": 89,
            },
        )

        if res.status_code != 201:
            raise RuntimeError(
                "Judge0 did not return as expected, please ensure it is running and try again."
            )

        res_output = res.json()
        test_results = json.loads(res_output["stdout"])
        print(test_results)
        out_str = "Note: These tests may or may not be used in final score calculation.\n"
        for test in test_results["tests"]:
            if test["status"] == "failed":
                if test["output"][-16:] == "invalid syntax\n\n":
                    # Invalid syntax needs stack trace cleanup
                    output_lines: list[str] = test["output"].splitlines()
                    lines_to_inlcude = [1, 8, 9, 10, 11]
                    out_str += f"Running tests failed due to a syntax error.\n{"\n".join([line for i,line in enumerate(output_lines) if i in lines_to_inlcude])}\n"
                else:   
                    # Runtime errors and test failures look good already
                    out_str += f"{test['name'].split(" ")[0]} {test['output']}"
            else:
                out_str += f"{test['name'].split(" ")[0]} passed!\n"

        return ConsoleLog(console_log=out_str[:-1])

        # else:
        #     sys.stdout.write(f"Error: {res.json()}")
        #     return ConsoleLog(console_log=f"Error: Submission Failed")

        # res = requests.get(f"http://host.docker.internal:2358/submissions/{token}")
        # if res.status_code == 200:
        #     actual_response = res.json()["stdout"]
        #     sys.stdout.write(f"\n\n{res.json()}\n\n")
        #     if actual_response is None:
        #         actual_response = ""
        #     return ConsoleLog(console_log=actual_response)
        # else:
        #     return ConsoleLog(console_log=f"Error: {res.json()["error"]} Submission")

    def package_submission(
        self, team_name: str, question_number: int, demo=False
    ) -> bytes:
        """Packages submission files into a string of a .zip contents.

        This packages together all files in autograder_utils
        as well as the `test_cases.py` (if demo = False) file for that question.
        With demo=True, `demo_cases.py` is packaged instead.
        """

        utils_dir = "backend/autograder_utils"
        question_dir = os.path.join("es_files", "questions", f"q{question_number}")

        with BytesIO() as f:  # Creates an in memory buffer we can use just like a file
            with ZipFile(
                f, "w"
            ) as new_zip:  # Creates a new zip in memory we can add to
                # Add all files in autograder_utils
                if not os.path.exists(utils_dir):
                    raise ResourceNotFoundException("No Utils Created.")

                for file in os.listdir(utils_dir):
                    new_zip.write(os.path.join(utils_dir, file), arcname=file)

                # Add test/demo case file
                if demo:
                    path = os.path.join(question_dir, "demo_cases.py")
                    if not os.path.exists(path):
                        raise ResourceNotFoundException(
                            f"Question {question_number} not found"
                        )
                    new_zip.write(path, arcname="demo_cases.py")
                else:
                    path = os.path.join(question_dir, "test_cases.py")
                    if not os.path.exists(path):
                        raise ResourceNotFoundException(
                            f"Demo cases for question {question_number} not found"
                        )
                    new_zip.write(path, arcname="test_cases.py")

                # Add submission file
                path = os.path.join(
                    submissions_dir, f"q{question_number}", f"{team_name}.py"
                )
                if not os.path.exists(path):
                    raise ResourceNotFoundException(
                        f"Team {team_name} did not submit question {question_number}"
                    )
                new_zip.write(path, arcname="submission.py")
            return base64.b64encode(f.getvalue())
