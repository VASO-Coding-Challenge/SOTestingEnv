"""Test cases for problem 1"""

import unittest
from submission import first_five
from decorators import weight

class Test(unittest.TestCase):

    @weight(1)
    def test_first_five(self):
        self.assertEqual(first_five("Hello World"), "Hello")

    @weight(1)
    def test_first_five(self):
        self.assertEqual(first_five("Bacon Cheeseburger"), "Bacon")
