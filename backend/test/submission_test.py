"""File to contain all Submission related tests"""

import os
from unittest.mock import patch
import pytest
from fastapi import HTTPException

from ..services import ProblemService
from ..services import SubmissionService
from ..test.fake_data.submission import setup_submission_data


__authors__ = ["Michelle Nguyen"]


def test_get_all_submissions(setup_submission_data):
    """Test retrieving all teams' submissions for all questions."""
    test_env = setup_submission_data()

    with patch(
        "backend.services.submissions.submissions_dir",
        str(test_env / "es_files" / "submissions"),
    ):
        with patch.object(ProblemService, "get_problems_list", return_value=[1, 2, 3]):
            submissions = SubmissionService.get_all_submissions()

            assert sorted(submissions.keys()) == ["A1", "B2", "C3"]

            assert 1 in submissions["A1"]
            assert 2 in submissions["A1"]
            assert 3 not in submissions["A1"]
            assert (
                submissions["A1"][1] == "def solve_q1_A1(): return 'A1 solution for q1'"
            )
            assert (
                submissions["A1"][2] == "def solve_q2_A1(): return 'A1 solution for q2'"
            )

            assert 1 in submissions["B2"]
            assert 2 not in submissions["B2"]
            assert 3 in submissions["B2"]

            assert 1 not in submissions["C3"]
            assert 2 in submissions["C3"]
            assert 3 in submissions["C3"]


def test_get_team_submissions(setup_submission_data):
    """Test retrieving a specific team's submissions for all questions."""
    test_env = setup_submission_data()

    with patch(
        "backend.services.submissions.submissions_dir",
        str(test_env / "es_files" / "submissions"),
    ):
        with patch.object(ProblemService, "get_problems_list", return_value=[1, 2, 3]):
            team_submissions = SubmissionService.get_team_submissions("A1")

            assert sorted(team_submissions.keys()) == [1, 2]
            assert (
                team_submissions[1] == "def solve_q1_A1(): return 'A1 solution for q1'"
            )
            assert (
                team_submissions[2] == "def solve_q2_A1(): return 'A1 solution for q2'"
            )

            team_submissions = SubmissionService.get_team_submissions("B2")

            assert sorted(team_submissions.keys()) == [1, 3]
            assert (
                team_submissions[1] == "def solve_q1_B2(): return 'B2 solution for q1'"
            )
            assert (
                team_submissions[3] == "def solve_q3_B2(): return 'B2 solution for q3'"
            )

            with pytest.raises(ValueError):
                SubmissionService.get_team_submissions("D4")


def test_get_specific_submission(setup_submission_data):
    """Test retrieving a specific team's submission for a specific question."""
    test_env = setup_submission_data()

    with patch(
        "backend.services.submissions.submissions_dir",
        str(test_env / "es_files" / "submissions"),
    ):
        # Test successful submission retrieval
        submission = SubmissionService.get_specific_submission("A1", 1)
        assert submission == "def solve_q1_A1(): return 'A1 solution for q1'"

        submission = SubmissionService.get_specific_submission("C3", 3)
        assert submission == "def solve_q3_C3(): return 'C3 solution for q3'"

        # Test non-existent submission for an existing team
        with pytest.raises(ValueError) as excinfo:
            SubmissionService.get_specific_submission("A1", 3)
        assert "No submission found for team A1 on problem 3" in str(excinfo.value)

        # Test submission for non-existent team
        with pytest.raises(ValueError) as excinfo:
            SubmissionService.get_specific_submission("D4", 1)
        assert "No submission found for team D4 on problem 1" in str(excinfo.value)

        # Test non-existent problem
        problem_path = test_env / "es_files" / "submissions" / "q4"
        if not problem_path.exists():
            with pytest.raises(ValueError) as excinfo:
                SubmissionService.get_specific_submission("A1", 4)
            assert "Problem 4 does not exist" in str(excinfo.value)
