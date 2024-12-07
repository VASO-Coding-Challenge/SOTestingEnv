import os
import pytest

__authors__ = ["Matthew Futch"]


@pytest.fixture
def setup_questions(tmp_path):
    def create_environment(number_of_questions=2):
        questions_dir = tmp_path / "es_files" / "questions"
        global_docs_dir = tmp_path / "es_files" / "global_docs"
        questions_dir.mkdir(parents=True)
        global_docs_dir.mkdir(parents=True)

        for i in range(1, number_of_questions + 1):
            question_dir = questions_dir / f"q{i}"
            question_dir.mkdir()

            prompt_file = question_dir / "prompt.md"
            local_doc_file = question_dir / "doc_foo.md"
            starter_code_file = question_dir / "starter.py"

            prompt_file.write_text(
                f"# Question {i}\nThis is the prompt for question {i}.",
                encoding="utf-8",
            )
            local_doc_file.write_text(
                f"# Documentation {i}\nThis is the test documentation for question {i} in testing.",
                encoding="utf-8",
            )
            starter_code_file.write_text("starter code")

        global_doc_file = global_docs_dir / "gd.md"
        global_doc_file.write_text(
            "# Global Docs\nThis is a global document.", encoding="utf-8"
        )

        return tmp_path

    return create_environment


@pytest.fixture
def setup_bad_questions(tmp_path):
    def create_bad_environment(number_of_questions=2):
        questions_dir = tmp_path / "es_files" / "questions"
        global_docs_dir = tmp_path / "es_files" / "global_docs"
        questions_dir.mkdir(parents=True)
        global_docs_dir.mkdir(parents=True)

        for i in range(1, number_of_questions + 1):
            question_dir = questions_dir / f"q{i}"
            question_dir.mkdir()

            prompt_file = question_dir / "prompt.md"
            local_doc_file = question_dir / "doc_foo.md"
            prompt_file.write_text(
                f"# Question {i}\nThis is the prompt for question {i}.",
                encoding="utf-8",
            )

            local_doc_file.write_text(
                f"# Documentation {i}\nThis is the test documentation for question {i} in testing.",
                encoding="utf-8",
            )
            os.chmod(
                local_doc_file, 0o000
            )  # sets file permissions to 000 (no read/write/execute)

        for i in range(1, 4):
            bad_doc_file = global_docs_dir / f"doc{i}.md"
            if i == 1:
                bad_doc_file.write_text(
                    "This document has restricted access."
                )  # change access perms
                os.chmod(bad_doc_file, 0o000)
            elif i == 2:
                bad_doc_file.write_bytes(
                    b"\x80\x81\x82Invalid binary content"
                )  # has binary data so cant read
            else:
                bad_doc_file.write_text("baddoc")
                os.rename(
                    bad_doc_file, global_docs_dir / f"doc{3}.png"
                )  # different file extension

        return tmp_path

    return create_bad_environment
