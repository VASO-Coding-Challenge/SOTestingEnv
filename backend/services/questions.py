"""Service to handle password generation and management"""

import os
from typing import List

from ..models import QuestionsPublic, Question, Document

__authors__ = ["Nicholas Almy"]


class QuestionService:
    """A service to handle questions for the competition"""

    def __init__(self):
        # Walk through the questions directory and load all the questions
        self.questions = self.load_questions()

    def get_questions(self) -> QuestionsPublic:
        """Get all the questions for the competition"""
        return self.questions

    def isQuestionDir(self, directory: str) -> bool:
        return directory.startswith("q") and directory[1:].isdigit()

    def isLocalDocumentationFile(self, file: str) -> bool:
        return file.startswith("doc_") and file.endswith(".md")

    def read_document(self, path: str, title: str) -> Document:
        try:
            with open(path, "r") as f:
                return Document(content=f.read(), title=title)
        except Exception as e:
            raise e

    def load_local_docs(self, question_num: int) -> List[Document]:
        local_docs_path = f"es_files/questions/q{question_num}"
        local_docs: List[Document] = []
        for doc in os.listdir(local_docs_path):
            if not self.isLocalDocumentationFile(doc):
                continue
            try:
                doc_title = doc[4:-3]
                local_docs.append(
                    self.read_document(os.path.join(local_docs_path, doc), doc_title)
                )
            except Exception as e:
                print(f"Could not process file {doc_title}")
        return local_docs

    def load_global_docs(self) -> List[Document]:
        global_docs_path = "es_files/global_docs"
        global_docs: List[Document] = []
        for doc in os.listdir(global_docs_path):
            if not doc.endswith(".md"):
                continue
            try:
                doc_title = doc[:-3]
                global_docs.append(
                    self.read_document(os.path.join(global_docs_path, doc), doc_title)
                )
            except Exception as e:
                print(f"Could not process file {doc_title}")
        return global_docs

    def load_question(self, question_num: int) -> Question:
        # Load the question
        question_path = f"es_files/questions/q{question_num}/prompt.md"
        try:
            with open(question_path, "r") as f:
                question = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Question {question_num} does not contain a prompt.md file"
            )

        # Get the documents for the question
        docs: List[Document] = self.load_local_docs(question_num)

        return Question(num=question_num, writeup=question, docs=docs)

    def load_questions(self):
        """Load all the questions from the questions directory"""
        # Get the current working directory
        questions_dir = "es_files/questions"
        questions: List[Question] = []
        # Walk through the directory and load all the questions (questions/q1/q1.md)
        for root, dirs, files in os.walk(questions_dir):
            for dir in dirs:
                # Skip non-question directories
                if not self.isQuestionDir(dir):
                    continue
                question_num = int(dir[1:])
                try:
                    question = self.load_question(question_num)
                    questions.append(question)
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise e

        # Load the global documents
        global_docs = self.load_global_docs()

        return QuestionsPublic(questions=questions, global_docs=global_docs)
