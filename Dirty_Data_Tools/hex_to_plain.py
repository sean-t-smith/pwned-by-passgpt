import sys

def is_non_printable(decoded_bytes):
    """Check if the decoded bytes contain any non-printable characters, excluding common whitespaces."""
    return not all(char.isprintable() or char in '\t' for char in decoded_bytes)

def decode_hex(password):
    """Decode a hexadecimal string unless decoding results in non-printable characters."""
    decoded = []
    multihex = filter(None, password.split("$"))
    for segment in multihex:
        if "HEX[" in segment:
            endhex = segment.find("]")
            if endhex == -1:
                return password, True  # Return original if no closing bracket.
            hex_data = segment[4:endhex]
            try:
                decoded_bytes = bytes.fromhex(hex_data).decode("utf-8")
                if is_non_printable(decoded_bytes):
                    return password, True  # Return original if non-printable characters found.
                decoded.append(decoded_bytes)
            except ValueError:
                return password, True  # Return original if hex decode fails.
        else:
            decoded.append(segment)
    return ''.join(decoded), False  # Return decoded string if no special conditions met.

def process_line(line):
    """Process a line, handling HEX decoding and ensuring no non-printable characters."""
    line_decoded = line.rstrip('\r\n')  # Strip CR and LF characters to manage newlines explicitly.
    parts = line_decoded.split(':')
    if len(parts) == 3 and "$HEX" in parts[2]:
        decoded_part, error = decode_hex(parts[2])
        if error:
            return parts[0] + ":" + parts[1] + ":" + decoded_part, True  # Keep original HEX segment if error.
        parts[2] = decoded_part  # Use decoded text.
        return ':'.join(parts), False
    return line_decoded, False

def process_large_file(input_file_path, output_file_path, error_file_path):
    """Process the input file, decoding hex-encoded passwords, ensuring no non-printable characters."""
    print("Starting processing...")
    line_count, hex_count, error_count = 0, 0, 0

    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
         open(output_file_path, 'w', encoding='utf-8') as output_file, \
         open(error_file_path, 'w', encoding='utf-8') as error_file:

        for line in input_file:
            line_count += 1
            processed_line, error_occurred = process_line(line)
            output_file.write(processed_line + '\n')  # Always write processed line to output.
            if not error_occurred:
                hex_count += 1  # Increment only if no error occurred during processing.
            else:
                error_count += 1
                error_file.write(processed_line + '\n')  # Log error lines.

            if line_count % 100000 == 0:
                print(f"Processed {line_count} lines. Successfully handled {hex_count} lines. Special cases: {error_count}")

    print(f"Processing complete. Total lines processed: {line_count}.")
    print(f"Successfully handled lines: {hex_count}. Special cases logged: {error_count}.")
    print("Output and errors written to:", output_file_path, "and", error_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_file> <error_file>")
        sys.exit(1)

    input_file_path, output_file_path, error_file_path = sys.argv[1:4]
    process_large_file(input_file_path, output_file_path, error_file_path)
