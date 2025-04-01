"""
A script to collect unique MPDT tags from all CoNLL files in a specified folder.
"""
import os
import glob
from typing import Dict

def collect_mpdt_tags(folder_path: str) -> Dict[str, int]:
    """Collect unique MPDT tags from all CoNLL files in the specified folder."""
    tag_counts : Dict[str, int] = {}
    # Find all .conll files in the specified folder (non-recursive)
    files = glob.glob(os.path.join(folder_path, "*.conll")) if os.path.isdir(folder_path) else [folder_path]
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments (starting with "#")
                if not line or line.startswith("#"):
                    continue
                parts = line.split('\t')
                # Check if the line has at least 5 columns (index 0-4)
                if len(parts) < 5:
                    continue
                # Assume that the original dependency is in column 5 (index 4)
                tag = parts[4].strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return tag_counts

def main() -> None:
    """Main function to execute the script."""
    folder = input("Specify the path to the folder with CoNLL files or a single CoNLL file: ").strip()
    if not os.path.isdir(folder) and not os.path.isfile(folder):
        print("The specified path is not a folder or does not exist.")
        return

    if os.path.isfile(folder):
        print("Processing file:", folder)
    else:
        print("Processing files from folder:", folder)
    tag_counts = collect_mpdt_tags(folder)
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[0])
    print(f"\nFound {len(sorted_tags)} unique tags:")
    for tag, count in sorted_tags:
        print(f"{tag} : {count}")

    output_file = "mpdt_tags_corrected.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for tag, count in sorted_tags:
            f.write(f"{tag}\t{count}\n")
    print(f"\nUnique tags along with their counts have been saved to the file: {output_file}")

if __name__ == "__main__":
    main()
