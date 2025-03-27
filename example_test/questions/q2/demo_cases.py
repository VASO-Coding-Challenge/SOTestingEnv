"Demo Cases for Problem 2"

import unittest
from submission import odd_chars

class Test(unittest.TestCase):

    def test_odd_chars1(self):
        self.assertEqual(odd_chars("Hello World"), "el ol")

    def test_odd_chars2(self):
        self.assertEqual(odd_chars("Hello World!"), "el ol!")

    def test_odd_chars3(self):
        self.assertEqual(odd_chars(" "), "")