"""Demo cases for problem 7"""

import unittest
from submission import find_value


class Test(unittest.TestCase):
    def test_find_value1(self):
        self.assertEqual(find_value(3), 6)

    def test_find_value2(self):
        self.assertEqual(find_value(4), 11)

    def test_find_value6(self):
        self.assertEqual(find_value(8), 125)