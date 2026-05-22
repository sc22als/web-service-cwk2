import requests
from bs4 import BeautifulSoup
import time
import json
import re

BASE_URL = "https://quotes.toscrape.com"
INDEX_FILE = "index.json"

def get_words(text):
    """Extracts words from text, makes them lowercase (case-insensitive)."""
    # Regex to find words, ignoring punctuation
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def build_index():
    """Crawls the site and builds the inverted index."""
    print("Starting build process. This will take a while due to the 6-second politeness window...")
    inverted_index = {}
    url_to_crawl = "/"
    
    while url_to_crawl:
        full_url = BASE_URL + url_to_crawl
        print(f"Crawling: {full_url}")
        
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text from the page
        page_text = soup.get_text()
        words = get_words(page_text)
        
        # Add to index (Simple frequency counting for the basic requirement)
        for word in set(words): # Get unique words on page
            if word not in inverted_index:
                inverted_index[word] = {}
            # Count frequency of the word on this specific page
            inverted_index[word][full_url] = words.count(word)
            
        # Find next page link
        next_btn = soup.find('li', class_='next')
        url_to_crawl = next_btn.find('a')['href'] if next_btn else None
        
        if url_to_crawl:
             print("Sleeping for 6 seconds to respect politeness window...")
             time.sleep(6) # CRITICAL REQUIREMENT

    # Save to file
    with open(INDEX_FILE, 'w') as f:
        json.dump(inverted_index, f)
    print("Index built and saved to", INDEX_FILE)

# --- You will need to build functions for load, print, and find next ---