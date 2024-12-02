"""Demo cases for problem 1"""

import unittest
from submission import first_five

class Test(unittest.TestCase):

    @weight(2)
    def test_first_five(self):
        self.assertEqual(first_five("Hello World"), "Hello")
