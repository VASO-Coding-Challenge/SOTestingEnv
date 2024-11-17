"""Service to handle the Submissions and interaction with Judge0 API"""

import os
from ..models import Submission, ConsoleLog


__authors__ = ["Nicholas Almy"]


class SubmissionService:
    """Service that deals with Submission CRUD operations"""

    def __init__(self):
        pass

    def submit(self, team_name: str, submission: Submission) -> None:
        """Submit a file to the submission folder... Only supports Python files"""
        submissions_dir = "es_files/submissions"
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

    def submit_and_run(self, team_name: str, submission: Submission) -> ConsoleLog:
        """Submit a file to the submission folder, runs it on a validation set and sends console logs back"""
        self.submit(team_name, submission)
        return self.run_submission(submission.question_num, team_name, forScore=False)

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
        # TODO: Run Judge0 API
        return ConsoleLog(console_log="Not Implemented...")
