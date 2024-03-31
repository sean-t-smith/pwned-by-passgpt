import os
import sys
from tqdm import tqdm

def process_ntlm_file(file_path, chunk_size=1024*1024*10):  # Process in 10MB chunks
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file_path = os.path.join(output_dir, 'no-occurrences_' + os.path.basename(file_path))

    with open(file_path, 'r', encoding='utf-8') as file:
        file_size = os.path.getsize(file_path)
        with open(output_file_path, 'w', encoding='utf-8') as out_file, \
                tqdm(total=file_size, desc="Processing NTLM Hashes", unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
            
            while True:
                lines = file.readlines(chunk_size)
                if not lines:
                    break

                for line in lines:
                    ntlm_hash = line.strip().split(':')[0]
                    out_file.write(ntlm_hash + '\n')

                progress_bar.update(len(''.join(lines)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <ntlm_file>")
    else:
        process_ntlm_file(sys.argv[1])
