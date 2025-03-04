"""File to contain all Problem manipulation related tests"""

import os
import pytest
from ..services import ProblemService
from ..test.fake_data.problem import setup_problem_data, setup_invalid_problem_data


__authors__ = ["Michelle Nguyen"]


def test_load_problems(setup_problem_data):
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    problems = ProblemService.get_problems_list()
    assert len(problems) == 2
    assert problems == [1, 2]  # Expecting problem IDs 1 and 2


def test_load_problem_files(setup_problem_data):
    test_env = setup_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    problem_id = 1
    prompt = ProblemService.get_problem_file_content(problem_id, "prompt.md")
    assert "# Problem 1" in prompt

    starter_code = ProblemService.get_problem_file_content(problem_id, "starter.py")
    assert "def solution()" in starter_code


def test_load_invalid_problem_data(setup_invalid_problem_data):
    test_env = setup_invalid_problem_data()
    ProblemService.QUESTIONS_DIR = str(test_env / "es_files" / "questions")

    problem_id = 1
    with pytest.raises(PermissionError):
        ProblemService.get_problem_file_content(problem_id, "prompt.md")

    with pytest.raises(
        ValueError
    ):  # Assuming your service handles binary files incorrectly
        ProblemService.get_problem_file_content(problem_id, "test_cases.py")

    with pytest.raises(FileNotFoundError):
        ProblemService.get_problem_file_content(
            problem_id, "starter.py"
        )  # Renamed file
