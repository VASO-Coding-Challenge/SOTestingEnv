"""Entry of the backend for the SOTesting Environment. Sets up FastAPI and exception handlers"""

from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from .services.exceptions import (
    InvalidCredentialsException,
    ResourceNotFoundException,
    ResourceNotAllowedException,
)

from .api import team, auth, question, docs, submission, static_files, session_obj

__authors__ = ["Andrew Lockard", "Mustafa Aljumayli"]

description = """
This RESTful API is designed to allow Science Olympiad students to submit code for grading purposes as a part of a coding competition.
"""

app = FastAPI(
    title="Science Olympiad Testing Environment API",
    version="1.0.0",
    description=description,
    openapi_tags=[
        team.openapi_tags,
        auth.openapi_tags,
        question.openapi_tags,
        docs.openapi_tags,
        submission.openapi_tags,
        session_obj.openapi_tags,
    ],
)


app.add_middleware(GZipMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4400"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ! Plug in each separate API file here (make sure to import above)
feature_apis = [team, auth, question, docs, submission, session_obj]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

app.mount("/", static_files.CustomStatic(directory=Path("./frontend")))


# TODO: Add Custom HTTP response exception handlers here for any custom Exceptions we create
@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(
    request: Request, e: ResourceNotFoundException
):
    return JSONResponse(status_code=404, content={"message": str(e)})


@app.exception_handler(InvalidCredentialsException)
def invalid_credentials_exception_handler(
    request: Request, e: InvalidCredentialsException
):
    return JSONResponse(
        status_code=401,
        content={"message": str(e)},
    )


@app.exception_handler(ResourceNotAllowedException)
def resource_not_allowed_exception_handler(
    request: Request, e: ResourceNotAllowedException
):
    return JSONResponse(status_code=403, content={"message": str(e)})
