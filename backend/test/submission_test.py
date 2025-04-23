"""File to contain all Submission related tests"""

import base64
import json
import os
import pytest

from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch
from zipfile import ZipFile

from backend.models.submission import ConsoleLog, ScoredTest, Submission
from backend.models.team import Team
from backend.services.exceptions import ResourceNotFoundException
from ..services import ProblemService
from ..services import SubmissionService
from .fake_data.submission import setup_submission_data
from .fixtures import submission_svc


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
        
def test_package_submission(setup_submission_data, submission_svc):
    """Test that package_submission correctly creates a zip archive with the expected files"""
    temp_dir = setup_submission_data()
    team_name = "A1"
    question_number = 1

    utils_dir = temp_dir / "backend" / "autograder_utils"
    utils_dir.mkdir(parents=True, exist_ok=True)
    (utils_dir / "util.py").write_text("def helper():\n    pass")

    q_dir = temp_dir / "es_files" / "questions" / f"q{question_number}"
    q_dir.mkdir(parents=True, exist_ok=True)
    (q_dir / "test_cases.py").write_text("def test_case():\n    pass")

    # Create submissions directory
    submissions_dir = temp_dir / "es_files" / "submissions" / f"q{question_number}"
    submissions_dir.mkdir(parents=True, exist_ok=True)
    (submissions_dir / f"{team_name}.py").write_text("def solution():\n    pass")

    # Save current directory and change to temp_dir
    original_dir = os.getcwd()
    os.chdir(temp_dir)

    try:
        with patch(
            "backend.services.submissions.submissions_dir",
            str(temp_dir / "es_files" / "submissions"),
        ):

            zip_bytes = submission_svc.package_submission(team_name, question_number)

            assert isinstance(zip_bytes, bytes)

            # Decode and check zip contents
            with BytesIO(base64.b64decode(zip_bytes)) as zip_buffer:
                with ZipFile(zip_buffer, "r") as zip_file:
                    file_list = zip_file.namelist()

                    # Check that expected files are in the zip
                    assert "test_cases.py" in file_list
                    assert "submission.py" in file_list
                    assert "util.py" in file_list
    finally:
        os.chdir(original_dir)


def test_package_submission_demo_mode(setup_submission_data, submission_svc):
    """Test that package_submission correctly uses demo_cases.py in demo mode"""
    temp_dir = setup_submission_data()
    team_name = "A1"
    question_number = 1

    utils_dir = temp_dir / "backend" / "autograder_utils"
    utils_dir.mkdir(parents=True, exist_ok=True)
    (utils_dir / "util.py").write_text("def helper():\n    pass")

    q_dir = temp_dir / "es_files" / "questions" / f"q{question_number}"
    q_dir.mkdir(parents=True, exist_ok=True)
    (q_dir / "demo_cases.py").write_text("def demo_test():\n    pass")

    submissions_dir = temp_dir / "es_files" / "submissions" / f"q{question_number}"
    submissions_dir.mkdir(parents=True, exist_ok=True)
    (submissions_dir / f"{team_name}.py").write_text("def solution():\n    pass")

    original_dir = os.getcwd()
    os.chdir(temp_dir)

    try:
        with patch(
            "backend.services.submissions.submissions_dir",
            str(temp_dir / "es_files" / "submissions"),
        ):

            zip_bytes = submission_svc.package_submission(
                team_name, question_number, demo=True
            )

            with BytesIO(base64.b64decode(zip_bytes)) as zip_buffer:
                with ZipFile(zip_buffer, "r") as zip_file:
                    file_list = zip_file.namelist()

                    assert "demo_cases.py" in file_list
                    assert "test_cases.py" not in file_list
    finally:
        os.chdir(original_dir)


def test_package_submission_nonexistent_team(setup_submission_data, submission_svc):
    """Test that package_submission raises ResourceNotFoundException for non-existent team"""
    temp_dir = setup_submission_data()
    team_name = "nonexistent_team"
    question_number = 1

    utils_dir = temp_dir / "backend" / "autograder_utils"
    utils_dir.mkdir(parents=True, exist_ok=True)
    (utils_dir / "util.py").write_text("def helper():\n    pass")

    q_dir = temp_dir / "es_files" / "questions" / f"q{question_number}"
    q_dir.mkdir(parents=True, exist_ok=True)
    (q_dir / "test_cases.py").write_text("def test_case():\n    pass")

    original_dir = os.getcwd()
    os.chdir(temp_dir)

    try:
        with patch(
            "backend.services.submissions.submissions_dir",
            str(temp_dir / "es_files" / "submissions"),
        ):

            with pytest.raises(
                ResourceNotFoundException,
                match=f"Team {team_name} did not submit question {question_number}",
            ):
                submission_svc.package_submission(team_name, question_number)
    finally:
        os.chdir(original_dir)


def test_send_to_judge0(submission_svc):
    """Test that send_to_judge0 correctly sends submission to judge0 API"""
    mock_submission_zip = base64.b64encode(b"test zip content")

    # Mock successful response from judge0
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "stdout": json.dumps(
            {
                "tests": [
                    {
                        "name": "Test 1",
                        "status": "passed",
                        "score": 10,
                        "max_score": 10,
                    },
                    {
                        "name": "Test 2",
                        "status": "failed",
                        "score": 0,
                        "max_score": 10,
                        "output": "Error message",
                    },
                ]
            }
        )
    }

    with patch("requests.post", return_value=mock_response) as mock_post:
        result = submission_svc.send_to_judge0(mock_submission_zip)

        mock_post.assert_called_once_with(
            "http://host.docker.internal:2358/submissions?wait=true",
            headers={"Content-Type": "application/json"},
            json={
                "additional_files": mock_submission_zip.decode("utf-8"),
                "language_id": 89,
            },
        )

        assert len(result) == 2
        assert result[0]["name"] == "Test 1"
        assert result[0]["status"] == "passed"
        assert result[1]["name"] == "Test 2"
        assert result[1]["status"] == "failed"


def test_get_max_points(setup_submission_data, submission_svc):
    """Test that get_max_points correctly calculates total weight from test cases"""
    temp_dir = setup_submission_data()
    question_num = 1

    q_dir = temp_dir / "es_files" / "questions" / f"q{question_num}"
    q_dir.mkdir(parents=True, exist_ok=True)
    test_cases_content = """
def test_case1():
    '''Test case 1'''
    @weight(5.0)
    assert True

def test_case2():
    '''Test case 2'''
    @weight(10.0)
    assert True
    """
    (q_dir / "test_cases.py").write_text(test_cases_content)

    original_dir = os.getcwd()
    os.chdir(temp_dir)

    try:
        with patch("os.path.join", side_effect=os.path.join), patch(
            "os.path.exists", return_value=True
        ), patch("builtins.open", mock_open(read_data=test_cases_content)):

            max_points = submission_svc.get_max_points(question_num)

            assert max_points == 15.0

            with patch("builtins.open", side_effect=Exception("Should not be called")):
                cached_points = submission_svc.get_max_points(question_num)
                assert cached_points == 15.0
    finally:
        os.chdir(original_dir)


def test_grade_submission(submission_svc):
    """Test grade_submission functionality"""
    team_name = "A1"
    question_num = 1

    mock_test_results = [
        {"name": "Test 1", "status": "passed", "score": 5.0, "max_score": 5.0},
        {
            "name": "Test 2",
            "status": "failed",
            "score": 0.0,
            "max_score": 10.0,
            "output": "Failed assertion",
        },
    ]

    with patch.object(
        submission_svc, "package_submission", return_value=b"zip_content"
    ), patch.object(
        submission_svc, "send_to_judge0", return_value=mock_test_results
    ), patch.object(
        submission_svc, "get_max_points", return_value=15.0
    ):

        result = submission_svc.grade_submission(question_num, team_name)

        assert len(result) == 2
        assert isinstance(result[0], ScoredTest)
        assert result[0].test_name == "Test 1"
        assert result[0].score == 5.0
        assert result[0].max_score == 5.0
        assert result[0].console_log == "Passed"

        assert result[1].test_name == "Test 2"
        assert result[1].score == 0.0
        assert result[1].max_score == 10.0
        assert result[1].console_log == "Failed assertion"


def test_grade_submission_resource_not_found(submission_svc):
    """Test grade_submission when resources are not found"""
    team_name = "nonexistent_team"
    question_num = 1

    with patch.object(
        submission_svc,
        "package_submission",
        side_effect=ResourceNotFoundException("Test not found"),
    ), patch.object(submission_svc, "get_max_points", return_value=15.0):

        result = submission_svc.grade_submission(question_num, team_name)

        assert len(result) == 1
        assert result[0].score == 0.0
        assert result[0].max_score == 15.0
        assert "Failed to Run Grader: Test not found" in result[0].console_log


def test_run_submission(submission_svc):
    """Test run_submission functionality"""
    team_name = "A1"
    question_num = 1

    mock_test_results = [
        {"name": "Test 1", "status": "passed"},
        {"name": "Test 2", "status": "failed", "output": "Assertion Error"},
    ]

    with patch.object(
        submission_svc, "package_submission", return_value=b"zip_content"
    ), patch.object(
        submission_svc, "send_to_judge0", return_value=mock_test_results
    ), patch(
        "builtins.print"
    ):

        result = submission_svc.run_submission(question_num, team_name)

        assert isinstance(result, ConsoleLog)
        assert (
            "Note: These tests may or may not be used in final score calculation"
            in result.console_log
        )
        assert "Test passed!" in result.console_log
        assert "Assertion Error" in result.console_log


def test_submit(setup_submission_data, submission_svc):
    """Test submit functionality"""
    temp_dir = setup_submission_data()
    team_name = "new_team"
    question_num = 1
    file_contents = "def solution():\n    return 'new solution'"

    submission = MagicMock(spec=Submission)
    submission.question_num = question_num
    submission.file_contents = file_contents

    original_dir = os.getcwd()
    os.chdir(temp_dir)

    try:
        submissions_dir = temp_dir / "es_files" / "submissions" / f"q{question_num}"
        submissions_dir.mkdir(parents=True, exist_ok=True)

        with patch(
            "backend.services.submissions.submissions_dir",
            str(temp_dir / "es_files" / "submissions"),
        ):

            submission_svc.submit(team_name, submission)

            submission_path = os.path.join(
                "es_files", "submissions", f"q{question_num}", f"{team_name}.py"
            )
            assert os.path.exists(submission_path)

            with open(submission_path, "r") as f:
                saved_content = f.read()
                assert saved_content == file_contents
    finally:
        os.chdir(original_dir)


def test_submit_and_run(submission_svc):
    """Test submit_and_run functionality"""
    team_name = "test_team"
    team = Team(id=1, name=team_name)
    question_num = 1
    file_contents = "def solution():\n    return 'test solution'"

    submission = MagicMock(spec=Submission)
    submission.question_num = question_num
    submission.file_contents = file_contents

    expected_console_log = "Test output"
    mock_console_log = ConsoleLog(console_log=expected_console_log)

    with patch.object(submission_svc, "submit") as mock_submit, patch.object(
        submission_svc, "run_submission", return_value=mock_console_log
    ) as mock_run:

        result = submission_svc.submit_and_run(team, submission)

        mock_submit.assert_called_once_with(team_name, submission)
        mock_run.assert_called_once_with(question_num, team_name)
        assert result.console_log == expected_console_log
