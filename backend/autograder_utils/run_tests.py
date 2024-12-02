import unittest
from json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('.', pattern="*_cases.py")
    JSONTestRunner(visibility='visible').run(suite)