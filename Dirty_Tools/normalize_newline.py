import sys

def process_line(line):
    """Process a single line to normalize line endings to '\n'."""
    # Normalize line endings in the line
    return line.replace('\r\n', '\n').replace('\r', '\n')

def normalize_line_endings(input_file_path, output_file_path, error_file_path):
    """Normalize line endings with minimal memory usage."""
    print("Starting processing...")
    crlf_count, cr_count, line_count = 0, 0, 0

    try:
        with open(input_file_path, 'r', encoding='utf-8', errors='replace') as input_file, \
             open(output_file_path, 'w', encoding='utf-8') as output_file:

            for line in input_file:
                normalized_line = process_line(line)
                output_file.write(normalized_line)
                
                # Update counters
                if '\r\n' in line:
                    crlf_count += line.count('\r\n')
                if '\r' in line:
                    cr_count += line.count('\r') - line.count('\r\n')  # Adjust for \r\n counted as \r
                
                line_count += 1
                if line_count % 100000 == 0:
                    print(f"Processed {line_count} lines so far.")

    except IOError as e:
        print(f"IOError encountered: {e}")
        sys.exit(1)

    print(f"Finished processing. Total lines: {line_count}.")
    print(f"Lines with CRLF endings: {crlf_count}, Lines with CR endings: {cr_count}.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_file> <error_file>")
        sys.exit(1)

    input_file_path, output_file_path, error_file_path = sys.argv[1:4]
    normalize_line_endings(input_file_path, output_file_path, error_file_path)
