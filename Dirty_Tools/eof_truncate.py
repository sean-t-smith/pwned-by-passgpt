#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def save_after_string(file_path, search_string, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Construct the path for the output file in the output directory
    output_file_name = 'after_' + os.path.basename(file_path)
    output_file_path = os.path.join(output_dir, output_file_name)
    
    found_string = False

    # Open the input file in binary mode to handle different encodings
    with open(file_path, 'rb') as infile:
        # Determine the file size for the progress bar
        file_size = os.path.getsize(file_path)
        
        # Initialize the progress bar
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Scanning file") as pbar:
            # Initialize the output file outside the loop to avoid reopening it for each line
            with open(output_file_path, 'wb') as outfile:
                while True:
                    line = infile.readline()
                    if not line:
                        break  # End of file
                    pbar.update(len(line))  # Update progress
                    
                    if found_string:
                        # Write subsequent lines to the output file
                        outfile.write(line)
                    elif search_string.encode('utf-8') in line:
                        found_string = True
                        # Do not write the line containing the search string, start writing from the next line

    if found_string:
        print(f"Content after '{search_string}' has been saved to {output_file_path}.")
    else:
        # If the search string was not found, remove the empty output file and notify the user
        os.remove(output_file_path)
        print(f"The string '{search_string}' was not found in the file.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_wordlist_file>")
        sys.exit(1)
    
    wordlist_path = sys.argv[1]
    search_string = "STS4122152809"  # String to search for
    output_dir = "./output"  # Directory to store the output file
    save_after_string(wordlist_path, search_string, output_dir)
