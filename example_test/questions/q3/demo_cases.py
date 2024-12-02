"""Demo cases for problem 3"""

import unittest
from submission import check_palindrome

class Test(unittest.TestCase):
    def test_check_palindrome1(self):
        self.assertEqual(check_palindrome("HelloolleH"), True)

    def test_check_palindrome2(self):
        self.assertEqual(check_palindrome("Helloolleh"), True)

    def test_check_palindrome3(self):
        self.assertEqual(check_palindrome("FooBarnaBooF"), False)

    def test_check_palindrome4(self):
        self.assertEqual(check_palindrome("aaa baa"), False)

    def test_check_palindrome5(self):
        self.assertEqual(check_palindrome("0"), True)