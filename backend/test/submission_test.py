"""File to contain all Submission related tests"""

import os
from pathlib import Path
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


def test_delete_team_submissions(setup_submission_data):
    """Test deleting a specific team's submissions."""
    test_env = setup_submission_data()

    submissions_path = str(test_env / "es_files" / "submissions")

    with patch("backend.services.submissions.submissions_dir", submissions_path):
        with patch.object(ProblemService, "get_problems_list", return_value=[1, 2, 3]):

            # Ensure team A1 has submissions before deletion
            assert (Path(submissions_path) / "q1" / "A1.py").exists()
            assert (Path(submissions_path) / "q2" / "A1.py").exists()

            # Delete team A1's submissions
            result = SubmissionService.delete_submissions("A1")

            # Ensure files are deleted
            assert not (Path(submissions_path) / "q1" / "A1.py").exists()
            assert not (Path(submissions_path) / "q2" / "A1.py").exists()

            # Ensure other teams' submissions are unaffected
            assert (Path(submissions_path) / "q1" / "B2.py").exists()
            assert (Path(submissions_path) / "q2" / "C3.py").exists()
            assert (Path(submissions_path) / "q3" / "B2.py").exists()
            assert (Path(submissions_path) / "q3" / "C3.py").exists()

            # Check the return message
            assert result == "Deleted 2 submission(s) for team 'A1'."

            # Try deleting a team with no submissions
            result_no_submissions = SubmissionService.delete_submissions("D4")
            assert result_no_submissions == "No submissions found for deletion."


def test_delete_all_submissions_removes_everything(setup_submission_data):
    """Test that delete_all_submissions clears out all files and folders."""
    test_env = setup_submission_data()
    submissions_path = str(test_env / "es_files" / "submissions")

    # patch the global submissions_dir to point at our temp tree
    with patch("backend.services.submissions.submissions_dir", submissions_path):
        # sanity check: we should have some files in q1, q2, q3
        q1 = Path(submissions_path) / "q1"
        q2 = Path(submissions_path) / "q2"
        q3 = Path(submissions_path) / "q3"
        assert any(q1.iterdir())
        assert any(q2.iterdir())
        assert any(q3.iterdir())

        # call the method under test
        result = SubmissionService.delete_all_submissions()
        assert result == "All submissions deleted successfully."

        # the root submissions directory should still exist but be empty
        root = Path(submissions_path)
        assert root.exists(), "submissions_dir should still exist"
        assert not any(root.iterdir()), "submissions_dir should now be empty"

        # calling it again on an empty directory should still succeed
        result2 = SubmissionService.delete_all_submissions()
        assert result2 == "All submissions deleted successfully."


def test_delete_all_submissions_on_empty_dir(setup_submission_data):
    """Test delete_all_submissions when there are no submissions at all."""
    test_env = setup_submission_data()
    submissions_path = str(test_env / "es_files" / "submissions")

    # first clear everything so it's empty
    with patch("backend.services.submissions.submissions_dir", submissions_path):
        SubmissionService.delete_all_submissions()

        # now directory exists but is empty
        root = Path(submissions_path)
        assert root.exists()
        assert not any(root.iterdir())

        # second call should not raise and should return the same message
        result = SubmissionService.delete_all_submissions()
        assert result == "All submissions deleted successfully."
