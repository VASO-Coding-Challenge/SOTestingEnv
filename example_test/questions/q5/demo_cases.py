"""Demo Cases for Problem 5"""

import unittest
from submission import three_input_truth_table

class Test(unittest.TestCase):
    def test_three_input_truth_table1(self):
        self.assertEqual(three_input_truth_table(True, True, True), True)

    def test_three_input_truth_table2(self):
        self.assertEqual(three_input_truth_table(True, True, False), True)

    def test_three_input_truth_table3(self):
        self.assertEqual(three_input_truth_table(True, False, True), False)

    def test_three_input_truth_table4(self):
        self.assertEqual(three_input_truth_table(True, False, False), True)

    def test_three_input_truth_table5(self):
        self.assertEqual(three_input_truth_table(False, True, True), False)

    def test_three_input_truth_table6(self):
        self.assertEqual(three_input_truth_table(False, True, False), True)

    def test_three_input_truth_table7(self):
        self.assertEqual(three_input_truth_table(False, False, True), False)

    def test_three_input_truth_table8(self):
        self.assertEqual(three_input_truth_table(False, False, False), True)