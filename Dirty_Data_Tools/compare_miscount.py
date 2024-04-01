#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def normalize_hash(hash_str):
    """Normalize the hash by making it uppercase and stripping white spaces."""
    return hash_str.upper().strip()

def detect_hash_position(first_line):
    """Automatically detects the hash position based on the structure of the first line."""
    parts = first_line.strip().split(':')
    # Assuming hash is always followed by a colon, check where hash might be based on common patterns
    if len(parts) > 2:
        # Likely format with hash in the middle or at the start
        try:
            int(parts[0])  # If first part is an integer, hash is likely in the middle
            return 1
        except ValueError:
            return 0  # Otherwise, hash is at the start
    return 0  # Default to first part being the hash if above conditions fail

def read_hashes(file_path):
    """Reads and normalizes hashes from the file, automatically determining their position."""
    with open(file_path, 'r') as file:
        first_line = file.readline()
        hash_position = detect_hash_position(first_line)
        file.seek(0)  # Reset file pointer to start
        hashes = {normalize_hash(line.split(':')[hash_position]): line.strip() for line in file}
    return hashes

def compare_and_output(file1_hashes, file2_hashes, output_file_path):
    """Compare hashes from both files and output unique entries."""
    unique_hashes = set(file1_hashes.keys()).symmetric_difference(set(file2_hashes.keys()))
    with open(output_file_path, 'w') as output_file, tqdm(total=len(unique_hashes), desc="Outputting Differences") as pbar:
        for hash_part in unique_hashes:
            if hash_part in file1_hashes:
                output_file.write(file1_hashes[hash_part] + '\n')
            if hash_part in file2_hashes:
                output_file.write(file2_hashes[hash_part] + '\n')
            pbar.update(1)

def main(file1_path, file2_path, output_file_path):
    print("Reading and normalizing hashes from both files...")
    file1_hashes = read_hashes(file1_path)
    file2_hashes = read_hashes(file2_path)

    print("Comparing and outputting differences...")
    compare_and_output(file1_hashes, file2_hashes, output_file_path)

    print("Comparison complete. Differences have been written to:", output_file_path)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <file1_path> <file2_path> <output_file_path>")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
