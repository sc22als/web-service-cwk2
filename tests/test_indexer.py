import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from indexer import get_words

class TestIndexer(unittest.TestCase):
    
    def test_get_words_lowercase(self):
        """Test that words are converted to lowercase."""
        text = "Hello WORLD"
        self.assertEqual(get_words(text), ['hello', 'world'])
        
    def test_get_words_punctuation(self):
        """Test that punctuation is ignored."""
        text = "Good morning, friends! How are you?"
        expected = ['good', 'morning', 'friends', 'how', 'are', 'you']
        self.assertEqual(get_words(text), expected)
        
    def test_get_words_empty(self):
        """Test edge case with empty string."""
        self.assertEqual(get_words(""), [])

if __name__ == '__main__':
    unittest.main()