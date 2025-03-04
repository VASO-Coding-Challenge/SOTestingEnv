"""This API Route handles ES GUI functionality for creating and updating problems."""

from typing import List
from fastapi import APIRouter, HTTPException, Body
from ..services.problems import ProblemService
from ..models import ProblemResponse

__authors__ = ["Michelle Nguyen"]

openapi_tags = {
    "name": "Problems",
    "description": "Routes for Problem Create/Update retrieval",
}

api = APIRouter(prefix="/api/problems")


@api.get("/", response_model=List[int], tags=["Problems"])
def get_problems_list():
    """Get all problem numbers."""
    return ProblemService.get_problems_list()


@api.get("/all", response_model=List[ProblemResponse], tags=["Problems"])
def get_all_problem_details():
    """Retrieve all problems and their files/contents."""
    problem_ids = ProblemService.get_problems_list()
    return [ProblemService.get_problem(q_num) for q_num in problem_ids]


@api.get("/{q_num}", response_model=ProblemResponse, tags=["Problems"])
def get_problem_details(q_num: int):
    """Retrieve a specific problem's files/contents."""
    return ProblemService.get_problem(q_num)


# @api.get("/{q_num}/prompt.md", response_model=dict, tags=["Problems"])
# def get_prompt(q_num: int):
#     """Fetch a problem’s prompt."""
#     return {"content": ProblemService.read_file(q_num, "prompt.md")}


# @api.get("/{q_num}/starter.py", response_model=dict, tags=["Problems"])
# def get_starter_code(q_num: int):
#     """Fetch a problem’s starter code."""
#     return {"content": ProblemService.read_file(q_num, "starter.py")}


# @api.get("/{q_num}/test_cases.py", response_model=dict, tags=["Problems"])
# def get_test_cases(q_num: int):
#     """Fetch a problem’s test cases."""
#     return {"content": ProblemService.read_file(q_num, "test_cases.py")}


# @api.get("/{q_num}/demo_cases.py", response_model=dict, tags=["Problems"])
# def get_demo_cases(q_num: int):
#     """Fetch a problem’s demo cases."""
#     return {"content": ProblemService.read_file(q_num, "demo_cases.py")}


@api.post("/create/", response_model=dict, tags=["Problems"])
def create_problem():
    """Create a new problem."""
    q_num = ProblemService.create_problem()
    return {"message": f"Problem q{q_num} created successfully"}


# @api.put("/{q_num}/prompt.md", response_model=dict, tags=["Problems"])
# def update_prompt(q_num: int, content: str = Body(...)):
#     """Update a problem’s prompt."""
#     ProblemService.write_file(q_num, "prompt.md", content)
#     return {"message": "Prompt updated successfully"}


# @api.put("/{q_num}/starter.py", response_model=dict, tags=["Problems"])
# def update_starter_code(q_num: int, content: str = Body(...)):
#     """Update a problem’s starter code."""
#     ProblemService.write_file(q_num, "starter.py", content)
#     return {"message": "Starter code updated successfully"}


# @api.put("/{q_num}/test_cases.py", response_model=dict, tags=["Problems"])
# def update_test_cases(q_num: int, content: str = Body(...)):
#     """Update a problem’s test cases."""
#     ProblemService.write_file(q_num, "test_cases.py", content)
#     return {"message": "Test cases updated successfully"}


# @api.put("/{q_num}/demo_cases.py", response_model=dict, tags=["Problems"])
# def update_demo_cases(q_num: int, content: str = Body(...)):
#     """Update a problem’s demo cases."""
#     ProblemService.write_file(q_num, "demo_cases.py", content)
#     return {"message": "Demo cases updated successfully"}


@api.put("/{q_num}", response_model=dict, tags=["Problems"])
def update_problem_files(
    q_num: int,
    prompt: str = Body(...),
    starter_code: str = Body(...),
    test_cases: str = Body(...),
    demo_cases: str = Body(...),
):
    """Update all files of a specific problem."""
    ProblemService.update_problem(q_num, prompt, starter_code, test_cases, demo_cases)
    return {"message": f"Problem {q_num} updated successfully."}


@api.delete("/{q_num}", response_model=dict, tags=["Problems"])
def delete_problem(q_num: int):
    """Delete a problem"""
    ProblemService.delete_problem(q_num)
    return {"message": f"Problem {q_num} deleted successfully."}


@api.delete("/", response_model=dict, tags=["Problems"])
def delete_all_problems():
    """Delete all problems."""
    try:
        while True:
            problem_ids = ProblemService.get_problems_list()
            if not problem_ids:
                break  # Stop when all problems are deleted

            for q_num in problem_ids[:]:  # Copy list to avoid modification issues
                try:
                    ProblemService.delete_problem(q_num)
                except HTTPException as e:
                    if e.status_code == 404:
                        continue  # Ignore and keep deleting
                    else:
                        raise  # Raise other unexpected errors

        return {"message": "All problems deleted successfully."}
    except Exception as e:
        # Handle any unexpected exceptions
        raise HTTPException(
            status_code=500, detail=f"Error deleting all problems: {str(e)}"
        )
