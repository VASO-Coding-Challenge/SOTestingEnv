import unittest
from json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    JSONTestRunner(visibility='visible').run(suite)