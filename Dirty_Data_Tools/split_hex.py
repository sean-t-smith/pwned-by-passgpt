import sys

def process_file(input_file_path, hex_output_file_path, non_hex_output_file_path):
    """Extracts lines with hexadecimal encoded passwords and other lines to separate files with verbose status updates."""
    line_count = 0
    hex_line_count = 0
    non_hex_line_count = 0

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(hex_output_file_path, 'w', encoding='utf-8') as hex_output_file, \
         open(non_hex_output_file_path, 'w', encoding='utf-8') as non_hex_output_file:
        
        for line in input_file:
            line_count += 1
            if "$HEX[" in line:
                hex_output_file.write(line)
                hex_line_count += 1
            else:
                non_hex_output_file.write(line)
                non_hex_line_count += 1
            
            if line_count % 100000 == 0:
                print(f"Processed {line_count} lines so far...")

    print(f"Processing complete. Total lines processed: {line_count}.")
    print(f"Total lines with hexadecimal encoded passwords: {hex_line_count}.")
    print(f"Total lines without hexadecimal encoded passwords: {non_hex_line_count}.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <hex_output_file> <non_hex_output_file>")
        sys.exit(1)
    
    input_file_path = sys.argv[1]
    hex_output_file_path = sys.argv[2]
    non_hex_output_file_path = sys.argv[3]
    
    print("Starting processing...")
    process_file(input_file_path, hex_output_file_path, non_hex_output_file_path)
    print("Check the output files for hexadecimal encoded lines and other lines.")
