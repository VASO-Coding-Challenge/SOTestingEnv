import os
import pytest

__authors__ = ["Michelle Nguyen"]


@pytest.fixture
def setup_problem_data(tmp_path):
    def create_problem_environment(problem_count=2):
        questions_dir = tmp_path / "es_files" / "questions"
        questions_dir.mkdir(parents=True)

        for i in range(1, problem_count + 1):
            question_dir = questions_dir / f"q{i}"
            question_dir.mkdir()

            # Create problem-related files
            (question_dir / "prompt.md").write_text(
                f"# Problem {i}\nSolve the problem described here.", encoding="utf-8"
            )
            (question_dir / "starter.py").write_text(
                f"# Starter code for Problem {i}\ndef solution():\n    pass",
                encoding="utf-8",
            )
            (question_dir / "test_cases.py").write_text(
                f"# Test cases for Problem {i}\ndef test_solution():\n    assert True",
                encoding="utf-8",
            )
            (question_dir / "demo_cases.py").write_text(
                f"# Demo cases for Problem {i}\ndef demo_case():\n    assert True",
                encoding="utf-8",
            )

        return tmp_path

    return create_problem_environment


@pytest.fixture
def setup_invalid_problem_data(tmp_path):
    def create_bad_environment(problem_count=2):
        questions_dir = tmp_path / "es_files" / "questions"
        questions_dir.mkdir(parents=True)

        for i in range(1, problem_count + 1):
            question_dir = questions_dir / f"q{i}"
            question_dir.mkdir()

            # Create a prompt but make it unreadable
            prompt_file = question_dir / "prompt.md"
            prompt_file.write_text(
                f"# Problem {i}\nUnreadable content", encoding="utf-8"
            )
            os.chmod(prompt_file, 0o000)  # No read permission

            # Corrupt test cases by adding binary data
            test_cases_file = question_dir / "test_cases.py"
            test_cases_file.write_bytes(b"\x80\x81\x82Invalid binary content")

            # Rename a required file to an incorrect extension
            starter_code_file = question_dir / "starter.py"
            starter_code_file.write_text("def broken_code(): pass", encoding="utf-8")
            os.rename(
                starter_code_file, question_dir / "starter.txt"
            )  # Wrong extension

        return tmp_path

    return create_bad_environment
