import sys

# List of required modules and their human-readable names
required_dependencies = {
    'torch': "PyTorch",
    'transformers': "Hugging Face Transformers"
}

missing_dependencies = []

# Attempt to import each module and check for errors
for module, readable_name in required_dependencies.items():
    try:
        __import__(module)
    except ImportError:
        missing_dependencies.append(readable_name)

# If there are missing dependencies, notify the user and exit
if missing_dependencies:
    missing_str = ", ".join(missing_dependencies)
    print(f"\nDependency Check: Failed | Missing: {missing_str}")
    print("Please install them using pip (e.g., `pip install torch transformers`) and try again.")
    sys.exit(1)
print("\nDependency Check: Successful")

# Import other modules after checking dependencies
from transformers import GPT2LMHeadModel, RobertaTokenizerFast
import torch
import os
import datetime
import time
import tempfile
import shutil

def is_cuda_available():
    """Check if CUDA is available."""
    return torch.cuda.is_available()

def get_device():
    """Get the execution device."""
    return torch.device("cuda" if is_cuda_available() else "cpu")

def initialize_model_and_tokenizer_10():
    """Initialize and return the model and tokenizer."""
    tokenizer = RobertaTokenizerFast.from_pretrained("javirandor/passgpt-10characters",
                                                     max_len=12,
                                                     padding="max_length", 
                                                     truncation=True,
                                                     do_lower_case=False,
                                                     strip_accents=False,
                                                     mask_token="<mask>",
                                                     unk_token="<unk>",
                                                     pad_token="<pad>",
                                                     truncation_side="right")

    model = GPT2LMHeadModel.from_pretrained("javirandor/passgpt-10characters").eval()

    device = get_device()
    model.to(device)
    return model, tokenizer

def initialize_model_and_tokenizer_16(api_token):
    """Initialize and return the model and tokenizer."""
    tokenizer = RobertaTokenizerFast.from_pretrained("javirandor/passgpt-16characters",
                                                     token=api_token,
                                                     max_len=18,
                                                     padding="max_length", 
                                                     truncation=True,
                                                     do_lower_case=False,
                                                     strip_accents=False,
                                                     mask_token="<mask>",
                                                     unk_token="<unk>",
                                                     pad_token="<pad>",
                                                     truncation_side="right")

    model = GPT2LMHeadModel.from_pretrained("javirandor/passgpt-16characters",
                                                    token=api_token).eval()

    device = get_device()
    model.to(device)
    return model, tokenizer

def generate_passwords(model, tokenizer, num_generations):
    """Generate passwords using the model and tokenizer."""
    start_time = time.time()

    device = get_device()
    generated = model.generate(torch.tensor([[tokenizer.bos_token_id]], device=device),
                               do_sample=True,
                               max_length=18,
                               num_return_sequences=num_generations,
                               pad_token_id=tokenizer.pad_token_id)

    end_time = time.time()
    print(f"Password generation complete. Time taken: {end_time - start_time:.2f} seconds.")
    return [password for password in tokenizer.batch_decode(generated, skip_special_tokens=True)]

def append_to_files_based_on_length(output_dir, passwords):
    """Append passwords to files based on their length, creating files if they don't exist."""
    for password in passwords:
        file_name = f"{len(password):02}-char-wordlist.txt"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(password + '\n')

def setup_output_directory():
    """Setup the output directory and placeholder files."""
    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in range(1, 18):
        with open(os.path.join(output_dir, f"{i:02}-char-wordlist.txt"), 'a', encoding='utf-8') as file:
            pass  # Creates the file if it doesn't exist

    return output_dir

def calculate_file_size(file_path):
    """Calculate and return the file size in a human-readable format."""
    file_size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if file_size < 1024:
            return f"{file_size}{unit}"
        file_size /= 1024
    return f"{file_size}GB"

def flush_to_disk(output_dir, file_name, passwords_batch):
    """Write a batch of passwords to the appropriate file."""
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'a', encoding='utf-8') as file:
        file.writelines(passwords_batch)

def log_error(output_dir, message):
    """Log an error message to a dedicated log file."""
    log_file_path = os.path.join(output_dir, 'error_log.txt')
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{timestamp}: {message}\n")

def distribute_asterisks(output_dir, append_counts):
    """
    Distributes asterisks as a visual indication of the distribution of passwords across files,
    mirroring the output style of the original script, including information on file sizes,
    appended lines, and a proportional asterisk distribution.
    """
    total_passwords = sum(len(passwords) for passwords in append_counts.values())
    asterisks_pool = 100  # Total number of asterisks to distribute
    file_summary = {}

    # Calculate initial distribution for each file
    for file_name, passwords in append_counts.items():
        proportion = len(passwords) / total_passwords if total_passwords > 0 else 0
        file_summary[file_name] = {
            "asterisks": round(proportion * asterisks_pool),
            "passwords": passwords
        }

    # Ensure the total asterisks count equals asterisks_pool
    asterisks_sum = sum(info["asterisks"] for info in file_summary.values())
    while asterisks_sum != asterisks_pool:
        for file_name, info in file_summary.items():
            if asterisks_sum > asterisks_pool and info["asterisks"] > 0:
                info["asterisks"] -= 1
                asterisks_sum -= 1
            elif asterisks_sum < asterisks_pool:
                info["asterisks"] += 1
                asterisks_sum += 1
            if asterisks_sum == asterisks_pool:
                break

    # Print the summary with formatted file size
    print("\nFile Name\t\tFile Size\tAppended Lines\tRun Distribution")
    for file_name, info in sorted(file_summary.items()):
        file_path = os.path.join(output_dir, file_name)
        file_size = format_file_size(file_path)
        asterisks = '*' * info["asterisks"]
        appended_lines = len(info["passwords"])
        print(f"{file_name}\t|{file_size}\t\t|{appended_lines}\t\t|{asterisks}")

def format_file_size(file_path):
    """
    Calculates the file size and returns a formatted string in KB, MB, GB, or TB.
    """
    file_size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if file_size < 1024.0:
            return f"{int(file_size)}{unit}"
        file_size /= 1024.0
    return f"{int(file_size)}PB"

def sort_and_deduplicate_file(original_file_path):
    """Sort the file content and deduplicate it by writing to a new file, with verbose status updates."""
    print(f"\tStarting to sort and deduplicate '{os.path.basename(original_file_path)}'...")

    # Step 1: Sort the file content
    print("\tSorting the file content...")
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_sorted_file, \
         open(original_file_path, 'r', encoding='utf-8') as original_file:
        sorted_lines = sorted(original_file)
        temp_sorted_file.writelines(sorted_lines)
    print("\tSorting complete.")

    # Step 2: Deduplicate while writing to a new file
    print("\tDeduplicating sorted content...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_dedup_file, \
         open(temp_sorted_file.name, 'r', encoding='utf-8') as sorted_file:
        previous_line = None
        line_count = 0
        for current_line in sorted_file:
            if current_line != previous_line:
                temp_dedup_file.write(current_line)
                previous_line = current_line
                line_count += 1
    print(f"\tDeduplication complete. {line_count} unique lines retained.")

    # Replace the original file with the deduplicated file
    os.replace(temp_dedup_file.name, original_file_path)
    # Clean up the sorted temporary file
    os.remove(temp_sorted_file.name)

def deduplicate_and_consolidate(output_dir):
    """Deduplicate all files in the output directory except 'error_log.txt' and consolidate them."""
    files = sorted([f for f in os.listdir(output_dir) if f != 'error_log.txt' and not f.startswith('passgpt-')])
    consolidated_path = os.path.join(output_dir, "passgpt-consolidated-wordlist.txt")

    for i, file_name in enumerate(files, start=1):
        file_path = os.path.join(output_dir, file_name)
        print(f"\nDeduplicating {file_name} ({i}/{len(files)})...")
        sort_and_deduplicate_file(file_path)
    
    with open(consolidated_path, 'w', encoding='utf-8') as consolidated_file:
        for file_name in files:
            file_path = os.path.join(output_dir, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                shutil.copyfileobj(f, consolidated_file)

def banner():
    # ASCII Art Banner for "PassGPT"
    print(r"""
     ____    WORDLIST      _____ _____ _______ 
    |  _ \   GENERATOR    / ____|  __ \__   __|
    | |_) | __ _ ___ ___ | |  __| |__) | | |   
    |  __/ / _` / __/ __|| | |_ |  ___/  | |   
    | |   | (_| \__ \__ \| |__| | |      | |   
    |_|    \__,_|___/___/ \_____|_|      |_|   
                                                
        """)
    print("START by running this script with no arguments:")
    print("   - On Windows:\tpython.exe passgpt_generator.py")
    print("   - On Mac/Linux:\tpython3 passgpt_generator.py\n")
    print("STOP this script by using the command:")
    print("   - On Windows:\tCtrl+C")
    print("   - On Mac:\t\tCmd+C\n")

def main():
    banner()
    output_dir = setup_output_directory()
    iteration = 0
    NUM_GENERATIONS = 1000

    print(f"Auto selecting best compute: {get_device()}")

    print(r"""
Please enter a number corresponding to your desired model:
          
    [1] Public  - javirandor/passgpt-10characters (Default) | huggingface.co/javirandor/passgpt-10characters
    [2] Private - javirandor/passgpt-16characters (Requires API Key) | huggingface.co/javirandor/passgpt-16characters
    """)

    model_choice = input("Enter Selection: ")

    if model_choice == '1':
        print("\nProceeding with 10 Char Model\n")
        model, tokenizer = initialize_model_and_tokenizer_10()
    elif model_choice == '2':
        print("\nProceeding with 16 Char Model")
        api_token = input("\nEnter API Key (Example: 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): ")
        print("\nWARNING: There is no input validation, hopefully you entered it correctly!\n")
        model, tokenizer = initialize_model_and_tokenizer_16(api_token)
    else:
        print("\nInvalid Input: Using Default Model (10 Chars)\n")
        model, tokenizer = initialize_model_and_tokenizer_10()

    try:
        while True:  # Infinite loop for continuous operation
            iteration += 1
            print(f"\nIteration {iteration}: Generating passwords, please wait...\n")
            passwords = generate_passwords(model, tokenizer, NUM_GENERATIONS)
            
            # Append passwords to files based on length, with error handling and batching
            append_counts = {f"{i:02}-char-wordlist.txt": [] for i in range(1, 18)}
            for password in passwords:
                length_file_name = f"{len(password):02}-char-wordlist.txt"
                try:
                    append_counts[length_file_name].append(password + '\n')
                    if len(append_counts[length_file_name]) >= 1000:  # Example batch size
                        flush_to_disk(output_dir, length_file_name, append_counts[length_file_name])
                        append_counts[length_file_name].clear()
                except KeyError as e:
                    log_error(output_dir, f"Error for password '{password}': {str(e)}")

            # Flush any remaining passwords not yet written to disk
            for file_name, passwords_batch in append_counts.items():
                if passwords_batch:
                    flush_to_disk(output_dir, file_name, passwords_batch)
            
            distribute_asterisks(output_dir, append_counts)
            
            print("\nPress Ctrl+C (Cmd+C on Mac) to gracefully end execution.")

    except KeyboardInterrupt:
        print("User initiated shutdown. Performing final steps before shutting down...")
        # Implement any necessary final steps here
        deduplicate_and_consolidate(output_dir)
        print(f"\nFinal steps complete, files written to: {output_dir}")
        # Exit the script
        sys.exit(0)

if __name__ == "__main__":
    main()