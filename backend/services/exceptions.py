"""This file contains custom exceptions in the service layer. These will then be handled approprately by the API layer"""


class ResourceNotFoundException(Exception):
    """Raised when a user attempts to access a resource that does not exist"""

    ...


class InvalidCredentialsException(Exception):
    """Raised when a user attempts to use an invalid authorization token"""

    ...


class ResourceNotAllowedException(Exception):
    """Raised when a user attempts to access a forbidden resource without valid permissions"""

    ...
