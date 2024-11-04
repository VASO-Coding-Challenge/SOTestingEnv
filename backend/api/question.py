from fastapi import APIRouter, Depends
from ..models import QuestionsPublic
from ..services.questions import QuestionService

openapi_tags = {
    "name": "Questions",
    "description": "Routes for Question retrieval",
}

api = APIRouter(prefix="/api/questions")


@api.get("/questions", response_model=QuestionsPublic, tags=["Questions"])
def get_questions():
    """Get all the questions for the competition"""
    question_svc = QuestionService()
    return question_svc.get_questions()
