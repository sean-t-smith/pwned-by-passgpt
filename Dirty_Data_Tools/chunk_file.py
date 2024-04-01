import os
import sys
from tqdm import tqdm

def divide_file_into_chunks(file_path, chunk_size_mb):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    chunk_size_bytes = chunk_size_mb * 1024 * 1024  # Convert MB to bytes
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    file_number = 1
    current_size = 0
    current_chunk = []

    file_size = os.path.getsize(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        with tqdm(total=file_size, desc="Dividing File", unit='B', unit_scale=True, unit_divisor=1024) as pbar:
            for line in file:
                line_size = len(line.encode('utf-8'))
                if current_size + line_size > chunk_size_bytes and current_chunk:
                    write_chunk(output_dir, file_number, chunk_size_mb, file_path, current_chunk)
                    file_number += 1
                    current_chunk = []
                    current_size = 0

                current_chunk.append(line)
                current_size += line_size
                pbar.update(line_size)

            # Write any remaining lines in the last chunk
            if current_chunk:
                write_chunk(output_dir, file_number, chunk_size_mb, file_path, current_chunk)

def write_chunk(output_dir, file_number, chunk_size_mb, file_path, chunk_lines):
    output_file_path = os.path.join(output_dir, f"{file_number:03}-{chunk_size_mb}MB_{os.path.basename(file_path)}")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(chunk_lines)
    print(f"Chunk {file_number} written to {output_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <hash_file> <chunk_size_in_MB>")
        sys.exit(1)

    hash_file = sys.argv[1]
    chunk_size_mb = int(sys.argv[2])
    divide_file_into_chunks(hash_file, chunk_size_mb)
