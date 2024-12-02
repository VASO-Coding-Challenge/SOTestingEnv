"""Demo Cases for Problem 4"""

import unittest
from submission import two_input_truth_table

class Test(unittest.TestCase):
    def test_two_input_truth_table1(self):
        self.assertEqual(two_input_truth_table(True, True), False)

    def test_two_input_truth_table2(self):
        self.assertEqual(two_input_truth_table(True, False), True)

    def test_two_input_truth_table3(self):
        self.assertEqual(two_input_truth_table(False, True), True)

    def test_two_input_truth_table4(self):
        self.assertEqual(two_input_truth_table(False, False), False)