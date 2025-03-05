# from fastapi import APIRouter, HTTPException
# from fastapi.responses import FileResponse
# import os

# __authors__ = ["Mustafa Aljumayli"]

# api = APIRouter(prefix="/docs")

# openapi_tags = {
#     "name": "Docs",
#     "description": "Routes for retrieving documents",
# }

# # Base path to the documentation files
# BASE_PATH = "/workspaces/SOTestingEnv/es_files"


# @api.get("/global_docs/{filename}", tags=["Docs"])
# async def get_global_doc(filename: str):
#     # Construct the path to the global document
#     path = os.path.join(BASE_PATH, "global_docs", f"doc_{filename}.md")
#     if not os.path.exists(path):
#         print(f"File not found: {path}")  # Debugging line
#         raise HTTPException(status_code=404, detail="File not found")
#     return FileResponse(path)


# # TEST ROUTE: http://localhost:4400/docs/global_docs/global


# @api.get("/questions/{question_num}/{filename}", tags=["Docs"])
# async def get_question_doc(question_num: int, filename: str):
#     # Construct the path to the question document
#     path = os.path.join(BASE_PATH, f"questions/q{question_num}", f"doc_{filename}.md")
#     print(f"Attempting to serve file at: {path}")  # Debugging line
#     if not os.path.exists(path):
#         print("File not found")  # Additional debug output
#         raise HTTPException(status_code=404, detail=f"File not found-{path}")
#     return FileResponse(path)  # Serve the file


# # TEST ROUTE: http://localhost:4402/docs/questions/2/q2

from fastapi import APIRouter, File, UploadFile, Form, Body, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from io import StringIO

from models.question import Document
from services.docs import DocsService

api = APIRouter(prefix="/docs")

openapi_tags = {
    "name": "Docs",
    "description": "Routes for retrieving documents",
}


@api.get("/", response_model=List[Document], tags=["Docs"])
async def get_all_documents():
    """Get all global documents."""
    return DocsService.get_documents()


@api.get("/{title}", response_model=Document, tags=["Docs"])
async def get_document(title: str):
    """Get a specific global document by title."""
    return DocsService.get_document(title)


@api.post("/", response_model=Document, tags=["Docs"])
async def upload_document_json(document: DocumentUpload):
    """Upload a document using JSON request body."""
    return DocsService.upload_document(document.content, document.title)


@api.post("/upload", response_model=Document, tags=["Docs"])
async def upload_document_form(
    file: UploadFile = File(...), title: Optional[str] = Form(None)
):
    """Upload a document using multipart form data."""
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode("utf-8")

        # Use filename from upload if title not provided
        if not title:
            # Remove extension from filename to use as title
            filename = file.filename
            if "." in filename:
                title = filename.rsplit(".", 1)[0]
            else:
                title = filename

        return DocsService.upload_document(content_str, title)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail=f"Error uploading document: {str(e)}"
        )


@api.delete("/{title}", tags=["Docs"])
async def delete_document(title: str):
    """Delete a global document."""
    return DocsService.delete_document(title)
