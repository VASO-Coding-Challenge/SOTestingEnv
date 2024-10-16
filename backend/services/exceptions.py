"""This file contains custom exceptions in the service layer. These will then be handled approprately by the API layer"""

class ResourceNotFoundException(Exception):
    """Raised when a user attempts to access a resource that does not exist"""
    ...

class UserPermissionException(Exception):
    """Raised when a logged in user attempts to access/modify a resource thats not allowed"""
    ...