"""Utility class for useful test helper methods"""

import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def captured_io(stdin):
    """Capture standard input and output, as well as standard error, and make that available for testing"""
    new_out, new_err, new_input = StringIO(), StringIO(), stdin
    old_out, old_err, old_input = sys.stdout, sys.stderr, sys.stdin
    try:
        sys.stdout, sys.stderr, sys.stdin = new_out, new_err, new_input
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr, sys.stdin = old_out, old_err, old_input


@contextmanager
def captured_output():
    """Capture standard error and output and make that available for testing"""
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def run_unittests(test_filename):
    """
    Use this method to discover unittests at specified path, and run them
    :param path:
    :return: TestResult
    """
    import unittest
    #TODO: redirect stderr to stdout for student unittests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_filename)

    runner = unittest.TextTestRunner(stream=sys.stdout)
    return runner.run(suite)
