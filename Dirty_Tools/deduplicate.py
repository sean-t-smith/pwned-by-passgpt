import os
import sys
from tqdm import tqdm

def deduplicate_file(file_path):
    output_dir = os.path.join(os.getcwd(), 'deduplicated')
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, os.path.basename(file_path))
    seen_lines = set()

    file_size = os.path.getsize(file_path)
    with open(file_path, 'r', encoding='utf-8') as file, \
         open(output_file_path, 'w', encoding='utf-8') as out_file, \
         tqdm(total=file_size, desc=f"Deduplicating {os.path.basename(file_path)}", unit='B', unit_scale=True, unit_divisor=1024) as pbar:

        for line in file:
            if line not in seen_lines:
                out_file.write(line)
                seen_lines.add(line)
            pbar.update(len(line.encode('utf-8')))

    print(f"Deduplicated file saved to {output_file_path}")

def deduplicate_folder():
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.txt'):
            deduplicate_file(filename)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path> or python script.py folder")
        sys.exit(1)

    if sys.argv[1] == "folder":
        deduplicate_folder()
    else:
        file_path = sys.argv[1]
        deduplicate_file(file_path)
