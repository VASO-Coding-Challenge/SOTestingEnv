"""File to contain all Question related tests"""

from ..models import Question, QuestionsPublic, Document
import os
import pytest
from .fixtures import question_svc
from ..test.fake_data.question import setup_questions, setup_bad_questions

__authors__ = ["Matthew Futch", "Michelle Nguyen"]


def test_isQuestionDir(question_svc):
    assert question_svc.isQuestionDir("q1000")
    assert not question_svc.isQuestionDir("1z")


def test_get_questions(question_svc, setup_questions):
    number_of_questions = 2
    tmp_path = setup_questions(number_of_questions)
    os.chdir(tmp_path)

    questions_public = question_svc.load_questions()

    assert questions_public == question_svc.get_questions()


def test_read_document(question_svc, setup_bad_questions):
    number_of_questions = 2
    tmp_path = setup_bad_questions(number_of_questions)
    os.chdir(tmp_path)

    with pytest.raises(Exception):  # read_document exception
        question_svc.read_document(
            f"{tmp_path}/es_files/questions/q1/doesntexist.extension", "foo"
        )


def test_load_global_docs(question_svc, setup_bad_questions):
    number_of_questions = 3
    tmp_path = setup_bad_questions(number_of_questions)
    os.chdir(tmp_path)

    assert len(question_svc.load_global_docs()) == 0


def test_refresh_questions(question_svc, setup_questions):
    number_of_questions = 2
    tmp_path = setup_questions(number_of_questions)
    os.chdir(tmp_path)

    startingQuestions = question_svc.load_questions()
    question_svc.refresh_questions()
    refreshedQuestions = question_svc.load_questions()

    assert startingQuestions.questions == refreshedQuestions.questions


def test_load_questions_file_not_found_error(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.remove(tmp_path / "es_files" / "questions" / "q1" / "prompt.md")
    os.chdir(tmp_path)

    try:
        question_svc.load_questions()
    except FileNotFoundError:
        pytest.fail("FileNotFoundError was not handled correctly")


def test_load_questions_file_fails_not_questionDir(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.mkdir(tmp_path / "es_files" / "questions" / "question1")
    os.chdir(tmp_path)

    assert question_svc.load_questions()


def test_load_question_with_no_starter_code(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.remove(tmp_path / "es_files" / "questions" / "q1" / "starter.py")
    os.chdir(tmp_path)
    assert (question_svc.load_question(1).starter_code) == ""


def test_load_questions_generic_exception(question_svc, setup_bad_questions):
    # Create a test environment that triggers a generic exception
    tmp_path = setup_bad_questions(2)
    os.chmod(
        tmp_path / "es_files" / "questions" / "q1" / "prompt.md", 0o000
    )  # Restrict permissions to cause an exception
    os.chdir(tmp_path)

    # Ensure the generic exception is raised correctly
    with pytest.raises(Exception):
        question_svc.load_questions()


def test_get_question_count(question_svc, setup_questions):
    """Test that get_question_count returns the correct number of questions"""
    tmp_path = setup_questions(
        number_of_questions=2
    )  # The function creates 2 questions by default

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        count = question_svc.get_question_count()

        assert count == 2
    finally:
        os.chdir(original_dir)


def test_load_starter_code(question_svc, setup_questions):
    """Test that load_starter_code correctly loads the starter code for a question"""
    tmp_path = setup_questions(number_of_questions=2)
    question_num = 1

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        starter_code = question_svc.load_starter_code(question_num)

        assert starter_code == "starter code"
    finally:
        os.chdir(original_dir)


def test_load_starter_code_file_not_found(question_svc, setup_questions):
    """Test that load_starter_code raises FileNotFoundError when starter code file doesn't exist"""
    tmp_path = setup_questions(number_of_questions=1)

    starter_file = tmp_path / "es_files" / "questions" / "q1" / "starter.py"
    os.unlink(starter_file)

    original_dir = os.getcwd()
    os.chdir(tmp_path)

    try:
        with pytest.raises(FileNotFoundError):
            question_svc.load_starter_code(1)
    finally:
        os.chdir(original_dir)
