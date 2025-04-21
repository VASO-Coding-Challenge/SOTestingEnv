"""File to contain all Problem manipulation related tests"""

import tempfile
import pytest
import shutil
import zipfile
import os
from pathlib import Path
from unittest.mock import patch
from fastapi import HTTPException
from ..services import ProblemService
from ..test.fake_data.problem import setup_problem_data


__authors__ = ["Michelle Nguyen"]


def test_get_problems_list(setup_problem_data):
    """Test retrieving the list of problems."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    problems = ProblemService.get_problems_list()
    assert len(problems) == 2
    assert problems == [1, 2]


def test_get_question_path(setup_problem_data):
    """Test getting the full path for a problem file."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    path = ProblemService.get_question_path(1, "prompt.md")
    assert os.path.basename(path) == "prompt.md"
    assert "q1" in path


def test_read_file(setup_problem_data):
    """Test reading a problem file."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    content = ProblemService.read_file(1, "prompt.md")
    assert content == "Prompt for problem 1"


def test_read_nonexistent_file(setup_problem_data):
    """Test reading a nonexistent file raises an HTTPException."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    with pytest.raises(HTTPException) as excinfo:
        ProblemService.read_file(1, "nonexistent.txt")

    assert excinfo.value.status_code == 404


def test_write_file(setup_problem_data):
    """Test writing a file to a problem directory."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    ProblemService.write_file(1, "new_file.txt", "Test content")

    path = ProblemService.get_question_path(1, "new_file.txt")
    assert os.path.exists(path)
    with open(path, "r") as f:
        assert f.read() == "Test content"


def test_get_problem(setup_problem_data):
    """Test retrieving full problem details."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    problem = ProblemService.get_problem(1)
    assert problem.num == 1
    assert problem.prompt == "Prompt for problem 1"
    assert problem.starter_code == "# Starter code for problem 1"
    assert problem.test_cases == "# Test cases for problem 1"
    assert problem.demo_cases == "# Demo cases for problem 1"


def test_create_problem(setup_problem_data):
    """Test creating a new problem."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    new_problem_num = ProblemService.create_problem()
    assert len(ProblemService.get_problems_list()) == 3

    problem_dir = os.path.join(ProblemService.QUESTIONS_DIR, f"q{new_problem_num}")
    assert os.path.exists(os.path.join(problem_dir, "prompt.md"))
    assert os.path.exists(os.path.join(problem_dir, "starter.py"))
    assert os.path.exists(os.path.join(problem_dir, "test_cases.py"))
    assert os.path.exists(os.path.join(problem_dir, "demo_cases.py"))


def test_update_problem(setup_problem_data):
    """Test updating an existing problem."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    ProblemService.update_problem(
        1,
        "Updated Prompt",
        "Updated Starter Code",
        "Updated Test Cases",
        "Updated Demo Cases",
    )

    updated_problem = ProblemService.get_problem(1)
    assert updated_problem.prompt == "Updated Prompt"
    assert updated_problem.starter_code == "Updated Starter Code"
    assert updated_problem.test_cases == "Updated Test Cases"
    assert updated_problem.demo_cases == "Updated Demo Cases"


def test_delete_problem(setup_problem_data):
    """Test deleting a problem and renumbering."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    ProblemService.delete_problem(1)

    problems = ProblemService.get_problems_list()
    assert len(problems) == 1
    assert problems == [1]

    problem = ProblemService.get_problem(1)
    assert problem.prompt == "Prompt for problem 2"


def test_zip_all_problems(setup_problem_data):
    """Test if zip_all_problems correctly generates a ZIP file containing all problems."""
    test_env = setup_problem_data()

    with patch(
        "backend.services.ProblemService.QUESTIONS_DIR",
        str(test_env / "es_files" / "questions"),
    ):
        zip_path = ProblemService.zip_all_problems()

        assert Path(zip_path).exists(), "ZIP file was not created."
        assert zip_path.endswith(".zip"), "Generated file is not a ZIP archive."

        with zipfile.ZipFile(zip_path, "r") as zip_file:
            file_list = zip_file.namelist()

            expected_files = [
                "q1/prompt.md",
                "q1/starter.py",
                "q1/test_cases.py",
                "q1/demo_cases.py",
                "q2/prompt.md",
                "q2/starter.py",
                "q2/test_cases.py",
                "q2/demo_cases.py",
            ]

            for expected_file in expected_files:
                assert (
                    expected_file in file_list
                ), f"Missing file in ZIP: {expected_file}"

        shutil.rmtree(test_env)


def test_get_problems_nonexistent_dir(setup_problem_data):
    """Test retrieving problems when the directory doesn't exist."""
    test_env = setup_problem_data()

    # Point to a nonexistent directory
    original_dir = ProblemService.QUESTIONS_DIR
    ProblemService.QUESTIONS_DIR = str(test_env / "nonexistent_dir")

    try:
        # Exercise
        problems = ProblemService.get_problems_list()

        # Verify
        assert problems == []
    finally:
        # Restore the original directory
        ProblemService.QUESTIONS_DIR = original_dir


def test_get_problem_nonexistent(setup_problem_data):
    """Test retrieving a nonexistent problem."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    with pytest.raises(HTTPException) as excinfo:
        ProblemService.get_problem(999)  # Non-existent problem number

    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail


def test_read_file_error(setup_problem_data):
    """Test error handling when reading a file fails."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    # Create an unreadable file
    problem_dir = test_env / "es_files" / "questions" / "q1"
    file_path = problem_dir / "unreadable.md"
    file_path.touch()

    # Make it unreadable if possible (this might not work on all systems)
    try:
        file_path.chmod(0)  # Remove all permissions

        with pytest.raises(HTTPException) as excinfo:
            ProblemService.read_file(1, "unreadable.md")

        assert excinfo.value.status_code == 500
        assert "Error reading" in excinfo.value.detail
    finally:
        # Reset permissions so the file can be removed during cleanup
        file_path.chmod(0o644)


def test_write_file_error(setup_problem_data):
    """Test error handling when writing a file fails."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    # Make the directory read-only if possible
    problem_dir = test_env / "es_files" / "questions" / "q1"

    try:
        # Create a read-only directory
        readonly_dir = problem_dir / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o500)  # Read and execute only

        with pytest.raises(HTTPException) as excinfo:
            ProblemService.write_file(1, "readonly/file.txt", "Content")

        assert excinfo.value.status_code == 500
        assert "Error writing" in excinfo.value.detail
    finally:
        # Reset permissions for cleanup
        readonly_dir.chmod(0o755)


def test_update_problem_nonexistent(setup_problem_data):
    """Test updating a nonexistent problem."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    with pytest.raises(HTTPException) as excinfo:
        ProblemService.update_problem(
            999,  # Non-existent problem
            "Updated Prompt",
            "Updated Starter Code",
            "Updated Test Cases",
            "Updated Demo Cases",
        )

    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail


def test_delete_problem_nonexistent(setup_problem_data):
    """Test deleting a nonexistent problem."""
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    with pytest.raises(HTTPException) as excinfo:
        ProblemService.delete_problem(999)  # Non-existent problem

    assert excinfo.value.status_code == 404
    assert "not found" in excinfo.value.detail


def test_zip_all_problems_nonexistent_dir():
    """Test zipping problems when the directory doesn't exist."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_dir = ProblemService.QUESTIONS_DIR
        ProblemService.QUESTIONS_DIR = os.path.join(temp_dir, "nonexistent")

        try:
            with pytest.raises(HTTPException) as excinfo:
                ProblemService.zip_all_problems()

            assert excinfo.value.status_code == 404
            assert "No problems found" in excinfo.value.detail
        finally:
            ProblemService.QUESTIONS_DIR = original_dir
