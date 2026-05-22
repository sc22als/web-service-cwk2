import unittest
import sys
import os
import io
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from search import find_phrase

class TestSearch(unittest.TestCase):
    
    def setUp(self):
        """Set up a mock index for testing search logic."""
        self.mock_index = {
            "hello": {"url1": 1, "url2": 2},
            "world": {"url1": 1, "url3": 5},
            "python": {"url3": 1}
        }

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_single_word(self, mock_stdout):
        """Test finding a single word that exists."""
        find_phrase(self.mock_index, ["hello"])
        output = mock_stdout.getvalue()
        self.assertIn("url1", output)
        self.assertIn("url2", output)
        
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_multi_word_intersection(self, mock_stdout):
        """Test multi-word query where only one URL matches both."""
        find_phrase(self.mock_index, ["hello", "world"])
        output = mock_stdout.getvalue()
        self.assertIn("url1", output)
        self.assertNotIn("url2", output)
        self.assertNotIn("url3", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_find_missing_word(self, mock_stdout):
        """Test edge case where a word does not exist."""
        find_phrase(self.mock_index, ["hello", "missing"])
        output = mock_stdout.getvalue()
        self.assertIn("No pages found", output)

if __name__ == '__main__':
    unittest.main()