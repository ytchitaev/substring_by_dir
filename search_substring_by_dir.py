'''
python substring_by_dir.py --dir C:\git\dir\subdir\ --substring "dbo_" --print_path 
python substring_by_dir.py --dir C:\git\dir\subdir\ --substring "dbo_" --deduplicate --write_to_file result.txt

'''
import os
import argparse
import re

def read_file(filepath):
    """Reads a file and returns its contents as a list of lines."""
    with open(filepath, 'r', errors='ignore') as f:
        return f.readlines()

def find_substring_in_word(word, substring, seen, print_path, filepath, deduplicate):
    """Checks if the word contains the substring and handles deduplication."""
    if substring in word:
        if deduplicate:
            if word in seen:
                return None
            seen.add(word)
        return f"{filepath:<100} | String: {word}" if print_path else word
    return None

def process_file(filepath, substring, print_path, deduplicate):
    """Processes a file searching for a substring."""
    seen = set()
    results = []
    lines = read_file(filepath)
    for line in lines:
        for word in re.split('\s', line):
            result = find_substring_in_word(word, substring, seen, print_path, filepath, deduplicate)
            if result is not None:
                results.append(result)
    return results

def search_files(directory, substring, print_path, deduplicate):
    """Searches through all files in a directory for a substring."""
    results = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            results.extend(process_file(filepath, substring, print_path, deduplicate))
    return results

def write_results_to_file(results, filename):
    """Writes the results to a file."""
    with open(filename, 'w') as f:
        f.write('\n'.join(results))

def main():
    parser = argparse.ArgumentParser(description='Search files for a substring')
    parser.add_argument('--dir', type=str, required=True, help='Directory to search')
    parser.add_argument('--substring', type=str, required=True, help='Substring to search for')
    parser.add_argument('--print_path', action='store_true', help='Print the filepath of the found substring')
    parser.add_argument('--deduplicate', action='store_true', help='Deduplicate the results')
    parser.add_argument('--write_to_file', type=str, help='Write the results to a file')

    args = parser.parse_args()

    results = search_files(args.dir, args.substring, args.print_path, args.deduplicate)

    if args.write_to_file:
        write_results_to_file(results, args.write_to_file)
    else:
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
