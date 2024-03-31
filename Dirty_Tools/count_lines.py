import os
import mmap
import argparse

def count_lines_with_mmap_and_progress(filename):
    total_size = os.path.getsize(filename)
    with open(filename, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        lines = 0
        while mm.tell() < mm.size():
            buffer = mm.readline()
            lines += 1
            progress = (mm.tell() / total_size) * 100
            print(f"\rLines: {lines}, Progress: {progress:.2f}%", end='')

        mm.close()
    return lines

def main():
    parser = argparse.ArgumentParser(description='Count the number of lines in a file with progress indicator')
    parser.add_argument('filename', type=str, help='The file to be processed')
    args = parser.parse_args()

    number_of_lines = count_lines_with_mmap_and_progress(args.filename)
    print(f"\nThe file {args.filename} has {number_of_lines} lines.")

if __name__ == "__main__":
    main()
