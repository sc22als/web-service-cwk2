import json

def print_word(index_data, word):
    """
    Prints the inverted index entry (URLs and frequencies) for a specific word.
    Formats the output as pretty-printed JSON.
    """
    if word in index_data:
        print(json.dumps(index_data[word], indent=4))
    else:
        print(f"Word '{word}' not found in the index.")

def find_phrase(index_data, search_words):
    """
    Finds pages containing ALL words provided in the search phrase.
    Uses set intersections for efficient multi-word querying.
    """
    matching_pages = None
    
    for word in search_words:
        if word in index_data:
            # Get a set of all URLs where this specific word appears
            pages_with_word = set(index_data[word].keys())
            
            if matching_pages is None:
                # First word sets our initial pool of potential matching pages
                matching_pages = pages_with_word
            else:
                # Intersection ensures we only keep pages containing ALL checked words
                matching_pages = matching_pages.intersection(pages_with_word)
        else:
            # If even one word from the phrase isn't in the index, the phrase cannot exist
            matching_pages = set()
            break
            
    # Display the results
    if matching_pages:
        print(f"Found {len(matching_pages)} matching pages:")
        for page in matching_pages:
            print(f" - {page}")
    else:
        print("No pages found containing all those search terms.")