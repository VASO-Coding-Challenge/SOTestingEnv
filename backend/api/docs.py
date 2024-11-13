from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

__authors__ = ["Mustafa Aljumayli"]

api = APIRouter(prefix="/docs")

openapi_tags = {
    "name": "Docs",
    "description": "Routes for retrieving documents",
}

# Base path to the documentation files
BASE_PATH = "/workspaces/SOTestingEnv/es_files"


@api.get("/global_docs/{filename}", tags=["Docs"])
async def get_global_doc(filename: str):
    # Construct the path to the global document
    path = os.path.join(BASE_PATH, "global_docs", f"doc_{filename}.md")
    if not os.path.exists(path):
        print(f"File not found: {path}")  # Debugging line
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path)


# TEST ROUTE: http://localhost:4400/docs/global_docs/global


@api.get("/questions/{question_num}/{filename}", tags=["Docs"])
async def get_question_doc(question_num: int, filename: str):
    # Construct the path to the question document
    path = os.path.join(BASE_PATH, f"questions/q{question_num}", f"doc_{filename}.md")
    print(f"Attempting to serve file at: {path}")  # Debugging line
    if not os.path.exists(path):
        print("File not found")  # Additional debug output
        raise HTTPException(status_code=404, detail=f"File not found-{path}")
    return FileResponse(path)  # Serve the file


# TEST ROUTE: http://localhost:4402/docs/questions/2/q2
