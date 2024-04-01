#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def filter_wordlist(input_file, max_length=27):
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file_name = f"{max_length}-chars_or_less_{os.path.basename(input_file)}"
    output_file_path = os.path.join(output_dir, output_file_name)

    try:
        with open(input_file, 'r', encoding='utf-8') as infile, \
                open(output_file_path, 'w', encoding='utf-8') as outfile:
            # Use tqdm directly on the file object for progress feedback
            for line in tqdm(infile, desc="Processing", unit=' lines'):
                if len(line.strip()) <= max_length:
                    outfile.write(line)
    except IOError as e:
        print(f"An error occurred: {e.strerror}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_wordlist_file>")
        sys.exit(1)
    
    wordlist_path = sys.argv[1]
    filter_wordlist(wordlist_path)
