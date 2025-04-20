"""
Test cases for utility functions
"""

import unittest
from datetime import datetime
import sys
import os

# Add the parent directory to the path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils import sanitize_filename, format_filename


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""

    def test_sanitize_filename(self):
        """Test that sanitize_filename properly removes invalid characters"""
        # Test with invalid characters
        self.assertEqual(sanitize_filename('test<>:"/\\|?*'), 'test________')
        
        # Test with normal text
        self.assertEqual(sanitize_filename('normal text'), 'normal text')
        
        # Test with symbols and spaces
        self.assertEqual(sanitize_filename('file: with "quotes" and * symbols'),
                        'file_ with _quotes_ and _ symbols')

    def test_format_filename(self):
        """Test that format_filename creates properly formatted filenames"""
        # Create a test date
        test_date = datetime(2023, 5, 15)
        
        # Test basic filename formatting
        self.assertEqual(
            format_filename(test_date, 'Test Video', 'mp4'),
            '15-05-2023 - Test Video.mp4'
        )
        
        # Test with special characters in title
        self.assertEqual(
            format_filename(test_date, 'Test: Video? With* Symbols!', 'mp4'),
            '15-05-2023 - Test_ Video_ With_ Symbols_.mp4'
        )


if __name__ == '__main__':
    unittest.main() 