"""Models for simply testing application setup and demo purposes"""

from pydantic import BaseModel

class CountModel(BaseModel):
    count: int