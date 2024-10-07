"""This API route is only going to be used for demo and setup confirmation purposes."""

from fastapi import APIRouter
from ..models.count import CountModel

__authors__ = ["Andrew Lockard"]

openapi_tags = {
    "name" : "Counting",
    "description" : "These routes are only used for demo/setup confirmation purposes.",
}

api = APIRouter(prefix="/api/test")

count = 0

@api.get("/count", tags=["Counting"])
def get_count() -> CountModel:
    """Gets the Current Count"""
    return CountModel(count=count)

@api.post("/count", tags=["Counting"])
def add_count() -> CountModel:
    """Incriments the Count and returns the new count"""
    count += 1
    return CountModel(count=count)