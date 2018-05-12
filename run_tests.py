# -*- coding: utf-8 -*-

import unittest

import sys

from tests.example_test import ExampleTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(ExampleTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
