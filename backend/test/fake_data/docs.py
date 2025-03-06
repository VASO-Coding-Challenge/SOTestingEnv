import tempfile
import pytest
from pathlib import Path


__authors__ = ["Michelle Nguyen"]


@pytest.fixture
def setup_docs_data():
    """Create a temporary test environment with sample documents."""

    def create_docs_environment():
        temp_dir = Path(tempfile.mkdtemp())

        docs_dir = temp_dir / "es_files" / "global_docs"
        docs_dir.mkdir(parents=True, exist_ok=True)

        (docs_dir / "sample1.md").write_text("Content for sample document 1")
        (docs_dir / "sample2.md").write_text("Content for sample document 2")

        return temp_dir

    return create_docs_environment
