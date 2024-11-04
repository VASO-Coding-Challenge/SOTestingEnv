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

    def load_questions(self):
        """Load all the questions from the questions directory"""
        # Get the current working directory
        questions_dir = "es_files/questions"
        questions: List[Question] = []
        # Walk through the directory and load all the questions (questions/q1/q1.md)
        for root, dirs, files in os.walk(questions_dir):
            for dir in dirs:
                # Get the question number
                question_num = int(dir[1:])
                question_path = os.path.join(root, dir, "prompt.md")
                with open(question_path, "r") as f:
                    question = f.read()
                # Get the documents for the question
                docs: List[Document] = []
                for doc in os.listdir(os.path.join(root, dir)):
                    if doc.startswith("doc_"):
                        doc_title = doc[4:-3]
                        with open(os.path.join(root, dir, doc), "r") as f:
                            docs.append(Document(content=f.read(), title=doc_title))
                questions.append(
                    Question(num=question_num, writeup=question, docs=docs)
                )
        # Load the global documents
        global_docs_path = "es_files/global_docs"
        global_docs: List[Document] = []
        for doc in os.listdir(global_docs_path):
            with open(os.path.join(global_docs_path, doc), "r") as f:
                global_docs.append(Document(content=f.read(), title=doc))
        return QuestionsPublic(questions=questions, global_docs=global_docs)

    def get_questions(self) -> QuestionsPublic:
        """Get all the questions for the competition"""
        return self.questions
