"""Test Cases for Problem 5"""

import unittest
from submission import three_input_truth_table
from decorators import weight


class Test(unittest.TestCase):
    @weight(1)
    def test_three_input_truth_table1(self):
        self.assertEqual(three_input_truth_table(True, True, True), True)

    @weight(1)
    def test_three_input_truth_table2(self):
        self.assertEqual(three_input_truth_table(True, True, False), True)

    @weight(1)
    def test_three_input_truth_table3(self):
        self.assertEqual(three_input_truth_table(True, False, True), False)

    @weight(1)
    def test_three_input_truth_table4(self):
        self.assertEqual(three_input_truth_table(True, False, False), True)

    @weight(1)
    def test_three_input_truth_table5(self):
        self.assertEqual(three_input_truth_table(False, True, True), False)

    @weight(1)
    def test_three_input_truth_table6(self):
        self.assertEqual(three_input_truth_table(False, True, False), True)

    @weight(1)
    def test_three_input_truth_table7(self):
        self.assertEqual(three_input_truth_table(False, False, True), False)

    @weight(1)
    def test_three_input_truth_table8(self):
        self.assertEqual(three_input_truth_table(False, False, False), True)
