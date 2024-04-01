import os
import sys
from tqdm import tqdm

def process_password_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    output_dir = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_dir, exist_ok=True)

    total_processed = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        # Get total number of lines for progress bar
        total_lines = sum(1 for _ in file)
        file.seek(0)  # Reset file pointer to the beginning

        with tqdm(total=total_lines, desc="Processing Passwords", unit='passwords') as progress_bar:
            for password in file:
                password = password.strip()
                if password:
                    length_str = f"{len(password):02}"
                    output_file = f"{output_dir}/{length_str}-char-{os.path.basename(file_path)}"
                    with open(output_file, 'a', encoding='utf-8') as out_file:
                        out_file.write(password + '\n')
                    total_processed += 1
                progress_bar.update(1)

    print(f"Total passwords processed: {total_processed}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <password_file>")
    else:
        process_password_file(sys.argv[1])
