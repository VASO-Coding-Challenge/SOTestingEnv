"""File to contain all Problem manipulation related tests"""

import os
from fastapi import HTTPException
import pytest
from ..services import ProblemService
from ..test.fake_data.problem import setup_tmp_questions


__authors__ = ["Michelle Nguyen"]


def test_get_problems_list(setup_tmp_questions):
    problems = ProblemService.get_problems_list()
    assert problems == [1]


def test_get_problem(setup_tmp_questions):
    problem = ProblemService.get_problem(1)
    assert problem.num == 1
    assert problem.prompt == "Sample prompt"


def test_get_problem_not_found():
    with pytest.raises(HTTPException) as ctx:
        ProblemService.get_problem(99)
    assert ctx.value.status_code == 404


def test_read_file(setup_tmp_questions):
    content = ProblemService.read_file(1, "prompt.md")
    assert content == "Sample prompt"


def test_read_file_not_found(setup_tmp_questions):
    with pytest.raises(HTTPException) as ctx:
        ProblemService.read_file(1, "nonexistent.md")
    assert ctx.value.status_code == 404


def test_create_problem(setup_tmp_questions):
    new_q_num = ProblemService.create_problem()
    assert (setup_tmp_questions / f"q{new_q_num}").exists()


def test_update_problem(setup_tmp_questions):
    ProblemService.update_problem(
        1, "New prompt", "def updated(): pass", "import unittest", "import unittest"
    )
    assert ProblemService.read_file(1, "prompt.md") == "New prompt"


def test_delete_problem(setup_tmp_questions):
    ProblemService.delete_problem(1)
    assert not (setup_tmp_questions / "q1").exists()


def test_delete_problem_not_found():
    with pytest.raises(HTTPException) as ctx:
        ProblemService.delete_problem(99)
    assert ctx.value.status_code == 404
