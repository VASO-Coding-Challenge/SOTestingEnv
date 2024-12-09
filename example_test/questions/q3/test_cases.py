"""Demo cases for problem 3"""

import unittest
from submission import check_palindrome
from decorators import weight

class Test(unittest.TestCase):
    @weight(1)
    def test_check_palindrome1(self):
        self.assertEqual(check_palindrome("HelloolleH"), True)

    @weight(1)
    def test_check_palindrome2(self):
        self.assertEqual(check_palindrome("Helloolleh"), True)

    @weight(2)
    def test_check_palindrome3(self):
        self.assertEqual(check_palindrome("FooBarnaBooF"), False)

    @weight(2)
    def test_check_palindrome4(self):
        self.assertEqual(check_palindrome("aaa baa"), False)

    @weight(2)
    def test_check_palindrome5(self):
        self.assertEqual(check_palindrome("0"), True)