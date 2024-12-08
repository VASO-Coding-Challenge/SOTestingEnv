"""Demo Cases for Problem 4"""

import unittest
from submission import two_input_truth_table
from decorators import weight

class Test(unittest.TestCase):
    @weight(1)
    def test_two_input_truth_table1(self):
        self.assertEqual(two_input_truth_table(True, True), False)

    @weight(1)
    def test_two_input_truth_table2(self):
        self.assertEqual(two_input_truth_table(True, False), True)

    @weight(1)
    def test_two_input_truth_table3(self):
        self.assertEqual(two_input_truth_table(False, True), True)

    @weight(1)
    def test_two_input_truth_table4(self):
        self.assertEqual(two_input_truth_table(False, False), False)