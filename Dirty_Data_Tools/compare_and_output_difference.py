#!/usr/bin/env python3

import os
import sys
from tqdm import tqdm

def process_files(uncracked_folder, cracked_folder, output_base_folder):
    os.makedirs(output_base_folder, exist_ok=True)
    uncracked_output_folder = os.path.join(output_base_folder, "uncracked")
    cracked_output_folder = os.path.join(output_base_folder, "cracked")
    os.makedirs(uncracked_output_folder, exist_ok=True)
    os.makedirs(cracked_output_folder, exist_ok=True)
    
    error_output_path = os.path.join(cracked_output_folder, "error.txt")

    # Adjusted for binary mode
    uncracked_files = {file.split('_')[0]: file for file in os.listdir(uncracked_folder) if file.endswith('.txt')}
    cracked_files = {file.split('_')[0]: file for file in os.listdir(cracked_folder) if file.endswith('.txt')}

    for prefix, uncracked_file in tqdm(uncracked_files.items(), desc="Processing files"):
        second_file = cracked_files.get(prefix)
        if not second_file:
            continue  # Skip if no corresponding cracked file

        first_file_path = os.path.join(uncracked_folder, uncracked_file)
        second_file_path = os.path.join(cracked_folder, second_file)
        uncracked_output_path = os.path.join(uncracked_output_folder, f"{prefix}_uncracked.txt")
        cracked_output_path = os.path.join(cracked_output_folder, f"{prefix}_cracked.txt")

        hash_to_password = {}
        with open(second_file_path, 'rb') as f:  # Binary mode
            for line in f:
                try:
                    decoded_line = line.decode('utf-8').strip()
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        hash_to_password[parts[0].lower()] = parts[1]
                except UnicodeDecodeError:
                    pass  # Optionally log or handle lines that fail to decode

        with open(first_file_path, 'rb') as f1, \
             open(uncracked_output_path, 'w', encoding='utf-8') as out_uncracked, \
             open(cracked_output_path, 'w', encoding='utf-8') as out_cracked, \
             open(error_output_path, 'a', encoding='utf-8') as out_error:

            for line in f1:
                try:
                    decoded_line = line.decode('utf-8').strip()
                    parts = decoded_line.split(':', 1)
                    if len(parts) == 2:
                        occurance, ntlm_hash = parts[0], parts[1].lower()
                        if ntlm_hash in hash_to_password:
                            out_cracked.write(f"{occurance}:{ntlm_hash.upper()}:{hash_to_password[ntlm_hash]}\n")
                        else:
                            out_uncracked.write(f"{occurance}:{ntlm_hash.upper()}\n")
                except UnicodeDecodeError:
                    out_error.write(f"Error decoding line: {line}\n")  # Log binary line that couldn't be decoded

        print(f"Processed: {uncracked_file} & {second_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py <folder_containing_uncracked_hashes> <folder_containing_cracked_hashes> <output_folder>")
        sys.exit(1)

    uncracked_folder = sys.argv[1]
    cracked_folder = sys.argv[2]
    output_base_folder = sys.argv[3]

    process_files(uncracked_folder, cracked_folder, output_base_folder)
