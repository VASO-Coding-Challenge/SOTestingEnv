import tempfile
import pytest
from pathlib import Path


__authors__ = ["Michelle Nguyen"]


@pytest.fixture
def setup_problem_data():
    """Create a temporary test environment with sample problem directories."""

    def create_problem_environment():
        # Create a temporary directory
        temp_dir = Path(tempfile.mkdtemp())

        # Create questions subdirectory
        questions_dir = temp_dir / "es_files" / "questions"
        questions_dir.mkdir(parents=True, exist_ok=True)

        # Create sample problem directories
        (questions_dir / "q1").mkdir()
        (questions_dir / "q2").mkdir()

        # Create sample files for problems
        for q_num in [1, 2]:
            problem_dir = questions_dir / f"q{q_num}"

            # Create standard problem files
            (problem_dir / "prompt.md").write_text(f"Prompt for problem {q_num}")
            (problem_dir / "starter.py").write_text(
                f"# Starter code for problem {q_num}"
            )
            (problem_dir / "test_cases.py").write_text(
                f"# Test cases for problem {q_num}"
            )
            (problem_dir / "demo_cases.py").write_text(
                f"# Demo cases for problem {q_num}"
            )

            # Create a documentation file
            (problem_dir / "doc_example.md").write_text(
                f"Documentation for problem {q_num}"
            )

        return temp_dir

    return create_problem_environment
