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

# --- Functions for load, print, and find next ---

def main_loop():
    """The main interactive command-line interface."""
    print("Search Engine Tool initialised.")
    print("Available commands: build, load, print <word>, find <phrase>, exit")
    
    # This variable will hold our loaded index in memory
    index_data = None 

    while True:
        try:
            # Get user input, strip whitespace, and split into words
            user_input = input("> ").strip().split()
            
            # If the user just pressed Enter without typing, ignore it
            if not user_input:
                continue
                
            command = user_input[0].lower()
            args = user_input[1:] # Everything typed after the command
            
            if command == "exit" or command == "quit":
                print("Exiting programme...")
                break
                
            elif command == "build":
                build_index()
                
            elif command == "load":
                try:
                    with open(INDEX_FILE, 'r') as f:
                        index_data = json.load(f)
                    print("Index successfully loaded into memory.")
                except FileNotFoundError:
                    print("Error: index.json not found. Please run 'build' first.")
                    
            elif command == "print":
                if not index_data:
                    print("Error: Please 'load' the index first.")
                    continue
                if not args:
                    print("Error: Please specify a word to print (e.g., 'print nonsense').")
                    continue
                    
                word = args[0].lower()
                if word in index_data:
                    # Print the dictionary nicely formatted
                    print(json.dumps(index_data[word], indent=4))
                else:
                    print(f"Word '{word}' not found in the index.")
                    
            elif command == "find":
                if not index_data:
                    print("Error: Please 'load' the index first.")
                    continue
                if not args:
                    print("Error: Please specify a search phrase (e.g., 'find good friends').")
                    continue
                    
                # Process multi-word queries
                search_words = [w.lower() for w in args]
                matching_pages = None
                
                for word in search_words:
                    if word in index_data:
                        # Get all URLs where this word appears
                        pages_with_word = set(index_data[word].keys())
                        
                        if matching_pages is None:
                            # First word sets the initial baseline of pages
                            matching_pages = pages_with_word
                        else:
                            # Intersection keeps ONLY pages that have ALL the words
                            matching_pages = matching_pages.intersection(pages_with_word)
                    else:
                        # If even one word is missing from the index, the whole phrase fails
                        matching_pages = set()
                        break
                        
                if matching_pages:
                    print(f"Found {len(matching_pages)} matching pages:")
                    for page in matching_pages:
                        print(f" - {page}")
                else:
                    print("No pages found containing all those search terms.")
                    
            else:
                print(f"Unknown command: '{command}'")
                
        # Gracefully handle Ctrl+C
        except KeyboardInterrupt:
            print("\nExiting programme...")
            break

if __name__ == "__main__":
    # This tells Python to actually run the function when you execute the script
    main_loop()