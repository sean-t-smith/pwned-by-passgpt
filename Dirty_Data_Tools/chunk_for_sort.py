import sys
import os

def distribute_lines(input_file):
    print("Starting distribution based on Total_Occurrences...")
    filenames = [
        "01_gte_1000.txt", "02_gte_500_lt_1000.txt", "03_gte_50_lt_500.txt",
        "04_gte_25_lt_50.txt", "05_gte_10_lt_25.txt", "06_gte_5_lt_10.txt",
        "07_gte_3_lt_5.txt", "08_equals_2.txt", "09_equals_1.txt"
    ]
    files = {fname: open(fname, 'w', encoding='utf-8') for fname in filenames}
    files["error.txt"] = open("error.txt", 'w', encoding='utf-8')
    counters = {fname: 0 for fname in filenames}
    counters["error.txt"] = 0

    with open(input_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, start=1):
            key = determine_key(int(line.split(':')[0]))
            files[key].write(line)
            counters[key] += 1

            if i % 10000 == 0:
                print(f"Processed {i} lines...")

    # Close files and print stats
    for fname, file in files.items():
        file.close()
        print(f"Finished writing to {fname}: {counters[fname]} lines.")

def determine_key(total_occurrences):
    if total_occurrences >= 1000:
        return "01_gte_1000.txt"
    elif 500 <= total_occurrences < 1000:
        return "02_gte_500_lt_1000.txt"
    elif 50 <= total_occurrences < 500:
        return "03_gte_50_lt_500.txt"
    elif 25 <= total_occurrences < 50:
        return "04_gte_25_lt_50.txt"
    elif 10 <= total_occurrences < 25:
        return "05_gte_10_lt_25.txt"
    elif 5 <= total_occurrences < 10:
        return "06_gte_5_lt_10.txt"
    elif 3 <= total_occurrences < 5:
        return "07_gte_3_lt_5.txt"
    elif total_occurrences == 2:
        return "08_equals_2.txt"
    elif total_occurrences == 1:
        return "09_equals_1.txt"
    return "error.txt"

def sort_file(filename):
    print(f"Sorting {filename}...")
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines.sort(key=lambda x: (-int(x.split(':')[0]), x.split(':')[1]))
    sorted_filename = f"{os.path.splitext(filename)[0]}_sorted.txt"

    with open(sorted_filename, 'w', encoding='utf-8') as sorted_file:
        sorted_file.writelines(lines)
    
    os.remove(filename)  # Remove the original file
    print(f"Finished sorting. Sorted file: {sorted_filename}.")

def combine_files(output_file_path, filenames):
    print("Combining sorted files into the final output file...")
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for fname in sorted(filenames):
            sorted_fname = f"{os.path.splitext(fname)[0]}_sorted.txt"
            with open(sorted_fname, 'r', encoding='utf-8') as infile:
                for line in infile:
                    outfile.write(line)
            print(f"Added {sorted_fname} to {output_file_path}.")
    print(f"Successfully combined all files into {output_file_path}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
        sys.exit(1)

    input_file_path, output_file_path = sys.argv[1:3]

    distribute_lines(input_file_path)

    # Define filenames based on the distribution criteria
    distributed_filenames = [
        "01_gte_1000.txt", "02_gte_500_lt_1000.txt", "03_gte_50_lt_500.txt",
        "04_gte_25_lt_50.txt", "05_gte_10_lt_25.txt", "06_gte_5_lt_10.txt",
        "07_gte_3_lt_5.txt", "08_equals_2.txt", "09_equals_1.txt"
    ]

    # Sort each file
    for fname in distributed_filenames:
        sort_file(fname)

    # Combine the sorted files into the final output, excluding the error file
    combine_files(output_file_path, distributed_filenames)
    print("Processing complete.")
