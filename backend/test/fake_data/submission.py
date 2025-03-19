from pathlib import Path
import tempfile
import pytest


__authors__ = ["Michelle Nguyen"]


@pytest.fixture
def setup_submission_data():
    """Create a temporary test environment with sample submissions."""

    def create_submission_environment():
        temp_dir = Path(tempfile.mkdtemp())

        submissions_path = temp_dir / "es_files" / "submissions"

        for p_num in [1, 2, 3]:
            prob_dir = submissions_path / f"q{p_num}"
            prob_dir.mkdir(parents=True, exist_ok=True)

            if p_num == 1:
                (prob_dir / "A1.py").write_text(
                    "def solve_q1_A1(): return 'A1 solution for q1'"
                )
                (prob_dir / "B2.py").write_text(
                    "def solve_q1_B2(): return 'B2 solution for q1'"
                )
            elif p_num == 2:
                (prob_dir / "A1.py").write_text(
                    "def solve_q2_A1(): return 'A1 solution for q2'"
                )
                (prob_dir / "C3.py").write_text(
                    "def solve_q2_C3(): return 'C3 solution for q2'"
                )
            else:
                (prob_dir / "B2.py").write_text(
                    "def solve_q3_B2(): return 'B2 solution for q3'"
                )
                (prob_dir / "C3.py").write_text(
                    "def solve_q3_C3(): return 'C3 solution for q3'"
                )

        return temp_dir

    return create_submission_environment
