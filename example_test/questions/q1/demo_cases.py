"""Demo cases for problem 1"""

import unittest
from submission import first_five

class Test(unittest.TestCase):

    def test_first_five1(self):
        self.assertEqual(first_five("Hello World"), "Hello")
