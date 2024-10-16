"""This package will hold all of the application level logic in the form of classes that FastAPI will dependency inject

This file marks services as a package: https://docs.python.org/3/tutorial/modules.html#packages
"""

# * Note: Add all module names to this list and import for easier imports outside this module
__all__ = ["count", "team", "passwords", "exceptions"]

from .count import CountService
from .team import TeamService
from .passwords import PasswordService
from .exceptions import ResourceNotFoundException
