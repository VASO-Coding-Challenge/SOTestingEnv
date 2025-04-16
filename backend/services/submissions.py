"""Service to handle the Submissions and interaction with Judge0 API"""

import glob
import os
import json
from typing import Dict
import requests  # type: ignore
import base64
from io import BytesIO  # Creates an in-memory "file"
from zipfile import ZipFile

from backend.services.problems import ProblemService

from ..models import Submission, ConsoleLog, Team, ScoredTest
from backend.services.exceptions import ResourceNotFoundException

__authors__ = ["Nicholas Almy", "Andrew Lockard"]

submissions_dir = "es_files/submissions"


class SubmissionService:
    """Service that deals with Submission CRUD operations"""

    def __init__(self):
        self._max_points: dict[int, int] = (
            {}
        )  # Maps question numbers to their max amount of points

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
        return self.run_submission(submission.question_num, team.name)

    def run_submission(self, question_num: int, team_name: str) -> ConsoleLog:
        """Run a submission on an Autograder and return the console logs
        Args:
            question_num (int): The question number
            team_name (str): The team name
        Returns:
            ConsoleLog: The console log of the submission
        """
        submission_zip = self.package_submission(team_name, question_num, True)
        test_results = self.send_to_judge0(submission_zip)
        print(test_results)
        out_str = (
            "Note: These tests may or may not be used in final score calculation.\n"
        )
        for test in test_results:
            if test["status"] == "failed":
                if test["output"][-16:] == "invalid syntax\n\n":
                    # Invalid syntax needs stack trace cleanup
                    output_lines: list[str] = test["output"].splitlines()
                    lines_to_include = [1, 8, 9, 10, 11]
                    out_str += f"Running tests failed due to a syntax error.\n{"\n".join([line for i,line in enumerate(output_lines) if i in lines_to_include])}\n"
                else:
                    # Runtime errors and test failures look good already
                    out_str += f"{test['name'].split(" ")[0]} {test['output']}"
            else:
                out_str += f"{test['name'].split(" ")[0]} passed!\n"

        return ConsoleLog(console_log=out_str[:-1])

    def grade_submission(self, question_num: int, team_name: str) -> list[ScoredTest]:
        """Grades a students submission against test questions
        Args:
            question_num (int): the question number that we are trying to grade
            team_name (str): the name of the team that we are trying to grade

        Returns:
            list[ScoredTest]: a list of objects representing the scored tests
        """

        try:
            submission_zip = self.package_submission(team_name, question_num, False)
            test_results = self.send_to_judge0(submission_zip)
        except ResourceNotFoundException as e:
            return [
                ScoredTest(
                    console_log="Failed to Run Grader: " + str(e),
                    test_name=f"Question {question_num} Tests",
                    question_num=question_num,
                    score=0.0,
                    max_score=self.get_max_points(question_num),
                )
            ]

        # Tally up scores
        scored_tests = []
        for test in test_results:
            if test["status"] == "passed":
                scored_tests.append(
                    ScoredTest(
                        console_log="Passed",
                        test_name=test["name"],
                        score=float(test["score"]),
                        max_score=float(test["max_score"]),
                        question_num=question_num,
                    )
                )

            elif "score" in test.keys() and "max_score" in test.keys():
                scored_tests.append(
                    ScoredTest(
                        console_log=test["output"],
                        test_name=test["name"],
                        score=float(test["score"]),
                        max_score=float(test["max_score"]),
                        question_num=question_num,
                    )
                )

            else:
                # Syntax error of some sorts
                scored_tests.append(
                    ScoredTest(
                        console_log=test["output"],
                        test_name=test["name"],
                        score=0,
                        max_score=self.get_max_points(question_num),
                        question_num=question_num,
                    )
                )

        return scored_tests

    def get_max_points(self, question_num: int) -> float:
        """Gets the max amount of points for a question by scanning through the test_cases.py file"""
        try:
            return self._max_points[question_num]
        except KeyError:
            question_test_file = os.path.join(
                "es_files", "questions", f"q{question_num}", "test_cases.py"
            )
            total_weight = 0.0
            with open(question_test_file, "r") as f:
                for line in f:
                    if "@weight(" in line:
                        start = line.index("(") + 1
                        end = line.index(")")
                        total_weight += float(line[start:end].strip())
            self._max_points[question_num] = total_weight
            return total_weight

    def send_to_judge0(self, submission_zip: bytes):
        """Sends the submission zip to judge0
        Args:
            submission_zip: the zip file containing all code to be executed in the judge0 environment
        Returns:
            A list of tests in this JSON form: {"name": str, "score": int, "max_score": int, "status": str, "output": str (only included if test failed)}
        """
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
        return test_results["tests"]

    def package_submission(
        self, team_name: str, question_number: int, demo=False
    ) -> bytes:
        """Packages submission files into a string of a .zip contents.

        This packages together all files in autograder_utils
        as well as the `test_cases.py` (if demo = False) file for that question.
        With demo=True, `demo_cases.py` is packaged instead.

        This submission file is built according to the specs on the judge0 documentation
        and includes autograder utils from the gradescope_utils package.
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

    @staticmethod
    def get_team_submissions(team_name: str) -> Dict[int, str]:
        """
        Get all submissions for a specific team.

        Args:
            team_name (str): Team name (e.g., "B1").

        Returns:
            Dict[int, str]: Dictionary mapping problem numbers to submission file content.

        Raises:
            ValueError: If team has no submissions.
        """
        result = {}
        found_any = False

        problem_numbers = ProblemService.get_problems_list()

        for p_num in problem_numbers:
            problem_dir = os.path.join(submissions_dir, f"q{p_num}")
            submission_path = os.path.join(problem_dir, f"{team_name}.py")

            if os.path.exists(submission_path):
                found_any = True
                with open(submission_path, "r") as f:
                    result[p_num] = f.read()

        if not found_any:
            raise ValueError(f"No submissions found for team {team_name}")

        return result

    @staticmethod
    def get_all_submissions() -> Dict[str, Dict[int, str]]:
        """
        Get all submissions from all teams.

        Returns:
            Dict[str, Dict[int, str]]: Dictionary mapping team names to their submissions.
        """
        result = {}

        problem_numbers = ProblemService.get_problems_list()

        problem_dirs = [
            os.path.join(submissions_dir, f"q{p_num}") for p_num in problem_numbers
        ]

        all_teams = set()

        for problem_dir in problem_dirs:
            if os.path.exists(problem_dir):
                team_files = glob.glob(os.path.join(problem_dir, "*.py"))
                for team_file in team_files:
                    team_name = os.path.basename(team_file).replace(".py", "")
                    all_teams.add(team_name)

        for team_name in all_teams:
            try:
                team_submissions = SubmissionService.get_team_submissions(team_name)
                result[team_name] = team_submissions
            except (ValueError, Exception):
                continue

        return result

    @staticmethod
    def get_specific_submission(team_name: str, p_num: int) -> str:
        """
        Get a specific submission for a team and problem.

        Args:
            team_name (str): Team name (e.g., "B1").
            p_num (int): Problem number.

        Returns:
            str: Content of the submission file.

        Raises:
            ValueError: If submission does not exist.
        """
        problem_dir = os.path.join(submissions_dir, f"q{p_num}")
        submission_path = os.path.join(problem_dir, f"{team_name}.py")

        if not os.path.exists(problem_dir):
            raise ValueError(f"Problem {p_num} does not exist")

        if not os.path.exists(submission_path):
            raise ValueError(
                f"No submission found for team {team_name} on problem {p_num}"
            )

        with open(submission_path, "r") as f:
            return f.read()

    @staticmethod
    def delete_submissions(team_name: str):
        """
        Delete all submissions of a specific team.

        Args:
            team_name (str): Team name (e.g., "B1").

        Returns:
            str: Success message indicating how many submissions were deleted.
        """
        problem_numbers = ProblemService.get_problems_list()
        if not problem_numbers:
            return "No problems found in the system."

        deleted_count = 0

        for p_num in problem_numbers:
            problem_dir = os.path.join(submissions_dir, f"q{p_num}")
            submission_path = os.path.join(problem_dir, f"{team_name}.py")

            if os.path.exists(submission_path):
                try:
                    os.remove(submission_path)
                    deleted_count += 1

                    if not os.listdir(problem_dir):
                        os.rmdir(problem_dir)

                except Exception as e:
                    return f"Error deleting submission {submission_path}: {str(e)}"

        return (
            f"Deleted {deleted_count} submission(s) for team '{team_name}'."
            if deleted_count > 0
            else "No submissions found for deletion."
        )
