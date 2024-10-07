"""Entry of the backend for the SOTesting Environment. Sets up FastAPI and exception handlers"""

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

from .api import count

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
    ],
)

# Using GZip middleware is an internet standard for compressing HTML responses over the network
app.add_middleware(GZipMiddleware)

# ! Plug in each seprate API file here (make sure to import above)
feature_apis = [
    count,
]

for feature_api in feature_apis:
    app.include_router(feature_api.api)

# TODO: Mount the static website built from the react application so the FastAPI server can serve it

# TODO: Add Custom HTTP response exception handlers here for any custom Exceptions we create
