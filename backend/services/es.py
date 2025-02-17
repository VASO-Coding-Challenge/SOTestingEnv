"""Service to handle the ESs feature"""

from dotenv import load_dotenv
import os
from .exceptions import InvalidCredentialsException


__authors__ = ["Nicholas Boyer", "Ivan Wu"]

load_dotenv(os.path.join(os.getcwd(), "backend/.env.development"))


class ES:
    """Model to define the creation shape of the ES model"""

    name: str
    password: str

    def __init__(self, name: str, password: str):
        self.name = name
        self.password = password


class ESService:
    """Service that preforms actions on ES Table."""

    def __init__(self):
        pass

    def get_es_with_credentials(self, name: str, password: str) -> ES:
        """Gets ES with a ES name and password."""
        if name != os.getenv("ES_USERNAME") or password != os.getenv("ES_PASSWORD"):
            raise InvalidCredentialsException("Incorrect credentials. Please try again")
        else:
            return ES(name=name, password=password)
