import requests
from bs4 import BeautifulSoup
import time
from indexer import get_words, save_index

# The target website to crawl
BASE_URL = "https://quotes.toscrape.com"

def build_index():
    """
    Crawls the target website sequentially, processes the HTML,
    builds an inverted index, and saves it to disk.
    """
    print("Starting build process. This will take approx 1 minute...")
    
    # The inverted index maps words to the URLs they appear in, along with their frequency
    # Structure: { "word": { "url1": frequency, "url2": frequency } }
    inverted_index = {}
    url_to_crawl = "/"
    
    while url_to_crawl:
        full_url = BASE_URL + url_to_crawl
        print(f"Crawling: {full_url}")
        
        try:
            # Fetch the web page
            response = requests.get(full_url)
            response.raise_for_status() # Raise an exception for bad status codes (e.g., 404)
        except requests.RequestException as e:
            print(f"Error crawling {full_url}: {e}")
            break
            
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        page_text = soup.get_text()
        words = get_words(page_text)
        
        # Populate the inverted index
        for word in set(words):
            if word not in inverted_index:
                inverted_index[word] = {}
            # Store the frequency of the word on this specific page
            inverted_index[word][full_url] = words.count(word)
            
        # Look for the 'next' button to find the next page to crawl
        next_btn = soup.find('li', class_='next')
        url_to_crawl = next_btn.find('a')['href'] if next_btn else None
        
        # If there is another page, we MUST respect the politeness window
        if url_to_crawl:
             print("Sleeping for 6 seconds to respect politeness window...")
             time.sleep(6) # Crucial requirement to avoid overwhelming the server

    # Persist the built index to the file system
    save_index(inverted_index)
    print("Index built and saved to data/index.json")