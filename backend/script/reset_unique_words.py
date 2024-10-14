"""Script to reset the unique words list for password generation"""

from ..services.team import TeamService

__authors__ = ["Andrew Lockard", "Nicholas Almy"]

TeamService.reset_word_list()
