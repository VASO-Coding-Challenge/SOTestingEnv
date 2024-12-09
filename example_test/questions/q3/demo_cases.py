"""Demo cases for problem 3"""

import unittest
from submission import check_palindrome

class Test(unittest.TestCase):
    def test_check_palindrome1(self):
        self.assertEqual(check_palindrome("HelloolleH"), True)

    def test_check_palindrome3(self):
        self.assertEqual(check_palindrome("FooBarnaBooF"), False)