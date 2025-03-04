import pytest
import os
import shutil
from fastapi import HTTPException
from backend.services.problems import ProblemService

__authors__ = ["Michelle Nguyen"]


@pytest.fixture(scope="function")
def setup_tmp_questions(tmp_path):
    """Set up a sample problem directory using tmp_path."""
    test_dir = tmp_path / "test_questions"
    test_dir.mkdir()

    # Override ProblemService's directory for this test session
    ProblemService.QUESTIONS_DIR = str(test_dir)

    problem_path = test_dir / "q1"
    problem_path.mkdir()

    (problem_path / "prompt.md").write_text("Sample prompt")
    (problem_path / "starter.py").write_text("def sample(): pass")
    (problem_path / "test_cases.py").write_text("import unittest")
    (problem_path / "demo_cases.py").write_text("import unittest")

    yield test_dir  # Provide the temporary directory for tests to use

    shutil.rmtree(test_dir, ignore_errors=True)  # Cleanup after test
