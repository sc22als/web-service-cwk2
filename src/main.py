from crawler import build_index
from indexer import load_index
from search import print_word, find_phrase

def main_loop():
    """
    The main interactive command-line interface loop.
    Handles user input and routes to the appropriate module functions.
    """
    print("Search Engine Tool initialised.")
    print("Available commands: build, load, print <word>, find <phrase>, exit")
    
    # Stores the loaded index in memory during runtime
    index_data = None 

    while True:
        try:
            # Read user input, remove leading/trailing whitespace, and split by spaces
            user_input = input("> ").strip().split()
            
            # Ignore empty inputs (e.g., user just pressing Enter)
            if not user_input:
                continue
                
            command = user_input[0].lower()
            args = user_input[1:] # Everything typed after the main command
            
            # Routing logic for commands
            if command in ["exit", "quit"]:
                print("Exiting programme...")
                break
                
            elif command == "build":
                build_index()
                
            elif command == "load":
                try:
                    index_data = load_index()
                    print("Index successfully loaded into memory.")
                except FileNotFoundError:
                    print("Error: Index file not found in data/. Please run 'build' first.")
                    
            elif command == "print":
                # Validation checks
                if not index_data:
                    print("Error: Please 'load' the index first.")
                    continue
                if not args:
                    print("Error: Please specify a word to print.")
                    continue
                    
                print_word(index_data, args[0].lower())
                    
            elif command == "find":
                # Validation checks
                if not index_data:
                    print("Error: Please 'load' the index first.")
                    continue
                if not args:
                    print("Error: Please specify a search phrase.")
                    continue
                    
                find_phrase(index_data, [w.lower() for w in args])
                    
            else:
                print(f"Unknown command: '{command}'")
                
        # Gracefully handle Ctrl+C to avoid ugly traceback errors
        except KeyboardInterrupt:
            print("\nExiting programme...")
            break

# Standard Python boilerplate to run the script
if __name__ == "__main__":
    main_loop()