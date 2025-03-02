"""This API Route handles ES GUI functionality for creating and updating problems."""

from fastapi import APIRouter, HTTPException, Body
from ..services.problems import ProblemService
from ..models import ProblemResponse

__authors__ = ["Michelle Nguyen"]

openapi_tags = {
    "name": "Problems",
    "description": "Routes for Problem Create/Update retrieval",
}

api = APIRouter(prefix="/api/problems")


@api.post("/problems/create/", response_model=dict)
def create_problem():
    """Create a new problem."""
    q_num = ProblemService.create_problem()
    return {"message": f"Problem q{q_num} created successfully"}


@api.get("/problems/{q_num}", response_model=ProblemResponse)
def get_problem(q_num: int):
    """Retrieve all problem files."""
    return ProblemService.get_problem(q_num)


@api.get("/problems/{q_num}/prompt.md", response_model=dict)
def get_prompt(q_num: int):
    """Fetch a problem’s prompt."""
    return {"content": ProblemService.read_file(q_num, "prompt.md")}


@api.put("/problems/{q_num}/prompt.md", response_model=dict)
def update_prompt(q_num: int, content: str = Body(...)):
    """Update a problem’s prompt."""
    ProblemService.write_file(q_num, "prompt.md", content)
    return {"message": "Prompt updated successfully"}


@api.get("/problems/{q_num}/starter.py", response_model=dict)
def get_starter_code(q_num: int):
    """Fetch a problem’s starter code."""
    return {"content": ProblemService.read_file(q_num, "starter.py")}


@api.put("/problems/{q_num}/starter.py", response_model=dict)
def update_starter_code(q_num: int, content: str = Body(...)):
    """Update a problem’s starter code."""
    ProblemService.write_file(q_num, "starter.py", content)
    return {"message": "Starter code updated successfully"}


@api.get("/problems/{q_num}/test_cases.py", response_model=dict)
def get_test_cases(q_num: int):
    """Fetch a problem’s test cases."""
    return {"content": ProblemService.read_file(q_num, "test_cases.py")}


@api.put("/problems/{q_num}/test_cases.py", response_model=dict)
def update_test_cases(q_num: int, content: str = Body(...)):
    """Update a problem’s test cases."""
    ProblemService.write_file(q_num, "test_cases.py", content)
    return {"message": "Test cases updated successfully"}


@api.get("/problems/{q_num}/demo_cases.py", response_model=dict)
def get_demo_cases(q_num: int):
    """Fetch a problem’s demo cases."""
    return {"content": ProblemService.read_file(q_num, "demo_cases.py")}


@api.put("/problems/{q_num}/demo_cases.py", response_model=dict)
def update_demo_cases(q_num: int, content: str = Body(...)):
    """Update a problem’s demo cases."""
    ProblemService.write_file(q_num, "demo_cases.py", content)
    return {"message": "Demo cases updated successfully"}
