"""Entry of the backend for the SOTesting Environment. Sets up FastAPI and SQLModel"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    docs_url=f"/docs",
    openapi_url="/url_root/openapi.json",
    redoc_url=None)

@app.get("/api/hello")
def hello_world():
    return {"Hello", "I am a working project!"}