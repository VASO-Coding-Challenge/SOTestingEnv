"""File to contain all Problem manipulation related tests"""

import os
import pytest
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
