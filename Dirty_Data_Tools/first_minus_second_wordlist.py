#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def file_exists(file_path):
    """Check if a file exists at the given path."""
    return os.path.exists(file_path)

def compare_wordlists(first_wordlist_path, second_wordlist_path):
    """Compare two wordlists and write the difference to a file."""
    if not file_exists(first_wordlist_path) or not file_exists(second_wordlist_path):
        print("One or both of the wordlist files do not exist.")
        return

    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, 'filtered_' + os.path.basename(first_wordlist_path))

    print("Loading second wordlist into memory. Please wait...")
    with open(second_wordlist_path, 'r', encoding='utf-8') as second_file:
        second_wordlist = set(tqdm((line.strip() for line in second_file), desc="Loading second wordlist"))

    print("Filtering first wordlist...")
    with open(first_wordlist_path, 'r', encoding='utf-8') as first_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file:
        for line in tqdm(first_file, desc="Filtering first wordlist"):
            if line.strip() not in second_wordlist:
                output_file.write(line)

    print(f"Filtered file saved to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <first_wordlist_path> <second_wordlist_path>")
        sys.exit(1)

    first_wordlist_path = sys.argv[1]
    second_wordlist_path = sys.argv[2]
    compare_wordlists(first_wordlist_path, second_wordlist_path)
