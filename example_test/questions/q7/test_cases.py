"""Demo cases for problem 7"""

import unittest
from submission import find_value
from decorators import weight


class Test(unittest.TestCase):
    @weight(1)
    def test_find_value1(self):
        self.assertEqual(find_value(3), 6)

    @weight(1)
    def test_find_value2(self):
        self.assertEqual(find_value(4), 11)

    @weight(2)
    def test_find_value3(self):
        self.assertEqual(find_value(5), 20)

    @weight(1)
    def test_find_value4(self):
        self.assertEqual(find_value(6), 37)

    @weight(2)
    def test_find_value5(self):
        self.assertEqual(find_value(7), 68)

    @weight(1)
    def test_find_value6(self):
        self.assertEqual(find_value(8), 125)