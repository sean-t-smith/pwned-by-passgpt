import sys

def sort_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Sort lines based on the NTLM hash (which is the second part of each line)
        lines.sort(key=lambda x: x.split(':')[1])

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines)
        print("File sorted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]

    sort_file(input_file_path, output_file_path)
