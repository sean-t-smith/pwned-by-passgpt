import sys
from tqdm import tqdm

def normalize_hash(hash_bytes):
    """Normalize the hash for consistent comparison."""
    return hash_bytes.strip().upper()

def read_occurrences_file(filepath):
    """Reads the occurrences file in binary and returns a dictionary with NTLM hash as key and occurrence as value."""
    occurrences = {}
    with open(filepath, 'rb') as file:
        for line in tqdm(file, desc="Reading occurrences file", unit='lines'):
            parts = line.strip().split(b':')
            if len(parts) == 2:
                occurrences[normalize_hash(parts[1])] = parts[0]
    return occurrences

def read_cracked_file(filepath):
    """Reads the cracked hashes file in binary and returns a dictionary of NTLM hashes to plain text passwords."""
    hashes = {}
    with open(filepath, 'rb') as file:
        for line in tqdm(file, desc="Reading cracked hashes file", unit='lines'):
            parts = line.strip().split(b':')
            if len(parts) >= 2:
                hashes[normalize_hash(parts[0])] = parts[1]
    return hashes

def compare_and_output(occurrences, cracked_hashes, unmatched_occurrences_path, unmatched_cracked_path):
    """Compare and output unmatched occurrences in binary mode."""
    with open(unmatched_occurrences_path, 'wb') as unmatched_occurrences_file, \
         open(unmatched_cracked_path, 'wb') as unmatched_cracked_file:
        # Check for unmatched in occurrences
        for hash_val, occ in tqdm(occurrences.items(), desc="Checking unmatched in occurrences", unit='records'):
            if hash_val not in cracked_hashes:
                unmatched_occurrences_file.write(occ + b':' + hash_val + b'\n')
                
        # Check for unmatched in cracked hashes
        for hash_val, pwd in tqdm(cracked_hashes.items(), desc="Checking unmatched in cracked hashes", unit='records'):
            if hash_val not in occurrences:
                unmatched_cracked_file.write(hash_val + b':' + pwd + b'\n')

def main(occurrences_filepath, cracked_hashes_filepath, unmatched_occurrences_path, unmatched_cracked_path):
    print("Starting comparison...")
    occurrences = read_occurrences_file(occurrences_filepath)
    cracked_hashes = read_cracked_file(cracked_hashes_filepath)

    compare_and_output(occurrences, cracked_hashes, unmatched_occurrences_path, unmatched_cracked_path)
    print(f"Unmatched occurrences output to: {unmatched_occurrences_path}")
    print(f"Unmatched cracked hashes output to: {unmatched_cracked_path}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python script.py <occurrences_file> <cracked_hashes_file> <unmatched_occurrences_output> <unmatched_cracked_output>")
        sys.exit(1)

    occurrences_file, cracked_hashes_file, unmatched_occurrences_path, unmatched_cracked_path = sys.argv[1:5]
    main(occurrences_file, cracked_hashes_file, unmatched_occurrences_path, unmatched_cracked_path)
