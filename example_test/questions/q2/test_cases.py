"Demo Cases for Problem 2"

import unittest
from submission import odd_chars
from decorators import weight

class Test(unittest.TestCase):

    @weight(2)
    def test_odd_chars1(self):
        self.assertEqual(odd_chars("Hello World"), "el ol")

    @weight(2)
    def test_odd_chars2(self):
        self.assertEqual(odd_chars("Hello World!"), "el ol!")

    @weight(2)
    def test_odd_chars3(self):
        self.assertEqual(odd_chars(" "), "")