"""This API route is only going to be used for demo and setup confirmation purposes."""

from fastapi import APIRouter, Depends
from ..models.count import Count
from ..services.count import CountService

__authors__ = ["Andrew Lockard"]

openapi_tags = {
    "name" : "Counting",
    "description" : "These routes are only used for demo/setup confirmation purposes.",
}

api = APIRouter(prefix="/api/test/count")

count = 0

@api.get("", tags=["Counting"])
def get_all_counters(count_svc: CountService = Depends()) -> list[Count]:
    """Gets the Current Count"""
    return count_svc.get_counts()

@api.post("", tags=["Counting"])
def add_counter(counter: Count, count_svc: CountService = Depends()) -> None:
    """Adds a new counter to the database"""
    return count_svc.add_new_counter(counter)

@api.get("/{id}", tags=["Counting"])
def get_counter(id: int, count_svc: CountService = Depends()) -> Count:
    """Gets a counter with id, returns 404 error if it was not found"""
    return count_svc.get_count(id)

@api.put("/{id}/{new_count}", tags=["Counting"])
def update_counter(id: int, new_count: int, count_svc: CountService = Depends()) -> Count:
    """Updates a counter with the matching id to hold a count of new_count"""
    return count_svc.update_counter(id, new_count)

@api.delete("/{id}", tags=["Counting"])
def delete_counter(id: int, count_svc: CountService = Depends()) -> bool:
    """Attempts to delete a counter with id"""
    return count_svc.delete_counter(id)