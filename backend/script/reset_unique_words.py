"""Script to reset the unique words list for password generation"""

from ..services import PasswordService

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

PasswordService.reset_word_list()
