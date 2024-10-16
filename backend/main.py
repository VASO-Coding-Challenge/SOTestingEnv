"""Entry of the backend for the SOTesting Environment. Sets up FastAPI and exception handlers"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware

from .services.exceptions import ResourceNotFoundException, UserPermissionException

from .api import count, team

__authors__ = ["Andrew Lockard"]

description = """
This RESTful API is designed to allow Science Olympiad students to submit code for grading purposes as a part of a coding competition.
"""

app = FastAPI(
    title="Science Olympiad Testing Environment API",
    version="1.0.0",
    description=description,
    openapi_tags=[
        # ! Insert Tags Here
        count.openapi_tags,
        team.openapi_tags,
    ],
)

# Using GZip middleware is an internet standard for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# ! Plug in each seprate API file here (make sure to import above)
feature_apis = [
    count,
    team,
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# TODO: Mount the static website built from the react application so the FastAPI server can serve it

# TODO: Add Custom HTTP response exception handlers here for any custom Exceptions we create
@app.exception_handler(ResourceNotFoundException)
def resource_not_found_exception_handler(request: Request, e: ResourceNotFoundException):
    return JSONResponse(status_code=404, content={"message": str(e)})

@app.exception_handler(UserPermissionException)
def user_perm_exception_handler(request: Request, e: UserPermissionException):
    return JSONResponse(status_code=405, content={"message": str(e)})
