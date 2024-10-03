"""Entry of the backend for the SOTesting Environment. Sets up FastAPI and SQLModel"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/hello")
def hello_world():
    return {"Hello", "I am a working project!"}