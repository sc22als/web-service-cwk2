import re
import json

# Define the path where the index will be stored
INDEX_FILE = "data/index.json" 

def get_words(text):
    """
    Extracts alphanumeric words from text and converts them to lowercase.
    This ensures our search index is case-insensitive.
    """
    # \b matches word boundaries, \w+ matches 1 or more word characters
    return re.findall(r'\b\w+\b', text.lower())

def save_index(index_data):
    """Saves the Python dictionary index to a JSON file for persistence."""
    with open(INDEX_FILE, 'w') as f:
        json.dump(index_data, f)

def load_index():
    """Loads the JSON index file back into a Python dictionary."""
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)