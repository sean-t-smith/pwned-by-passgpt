import os
import sys
from tqdm import tqdm

def process_lines(lines, out_buffer, desired_length):
    for line in lines:
        if len(line) <= desired_length:
            out_buffer.append(line + '\n')

def write_buffer(out_file, out_buffer):
    out_file.writelines(out_buffer)
    out_buffer.clear()

def filter_wordlist_by_length(input_file, desired_length, chunk_size=1024 * 1024 * 100):  # 100 MB chunk
    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    output_file_name = f"{desired_length:02}-chars_{os.path.basename(input_file)}"
    output_file_path = os.path.join(output_dir, output_file_name)

    file_size = os.path.getsize(input_file)
    out_buffer = []

    with open(input_file, 'r', encoding='utf-8') as file, \
         open(output_file_path, 'w', encoding='utf-8') as out_file, \
         tqdm(total=file_size, desc="Filtering Wordlist", unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:

        buffer = ''
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break

            lines = (buffer + chunk).split('\n')
            buffer = lines.pop()
            process_lines(lines, out_buffer, desired_length)

            if len(out_buffer) >= 1000:  # Write in batches of 1000 lines
                write_buffer(out_file, out_buffer)

            progress_bar.update(len(chunk))

        process_lines([buffer], out_buffer, desired_length)  # Process any remaining line
        write_buffer(out_file, out_buffer)  # Write remaining buffer

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <wordlist_file> <desired_length>")
        sys.exit(1)

    wordlist_file = sys.argv[1]
    desired_length = int(sys.argv[2])
    filter_wordlist_by_length(wordlist_file, desired_length)
