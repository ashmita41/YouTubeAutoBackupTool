#!/usr/bin/env python3
"""
Run all unit tests for the YouTube Auto Backup application
"""

import unittest
import os
import sys

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def run_all_tests():
    """
    Discover and run all tests in the tests directory
    """
    # Start in the current directory and find all test modules
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests()) 