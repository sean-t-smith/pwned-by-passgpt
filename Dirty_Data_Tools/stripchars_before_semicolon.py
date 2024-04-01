#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def process_wordlist(input_file_path):
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file_name = 'processed_' + os.path.basename(input_file_path)
    output_file_path = os.path.join(output_dir, output_file_name)
    error_log_path = os.path.join(output_dir, 'error_log.txt')

    with open(input_file_path, 'rb') as infile, \
         open(output_file_path, 'w', encoding='utf-8') as outfile, \
         open(error_log_path, 'w', encoding='utf-8') as error_log:
        for line in tqdm(infile, desc="Processing wordlist"):
            try:
                # Attempt to decode each line as UTF-8
                decoded_line = line.decode('utf-8')
                processed_line = decoded_line.split(':', 1)[-1]
                outfile.write(processed_line)
            except UnicodeDecodeError:
                # Log undecodable lines to the error log
                error_log.write(f"Undecodable line at position {infile.tell()}: {line}\n")

    print(f"Processed wordlist saved to {output_file_path}")
    print(f"Errors logged to {error_log_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_wordlist_file>")
        sys.exit(1)
    
    wordlist_path = sys.argv[1]
    process_wordlist(wordlist_path)
