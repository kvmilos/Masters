"""
Corrector for MPDT CONLL files.
"""
import os
from utils.node import Node
from tests.corrector_tests import test_pos, test_feats, test_feats_pos_combination


def correct_conll_line(n: Node):
    """
    Corrects a line of a CONLL file.
    """
    # If POS has extra features appended, remove them
    if ':' in n.pos:
        n.pos = n.pos.split(":")[0]

    # Print a warning if POS is not in pos_list
    test_pos(n.pos)

    # Check if pos_feats and feats have exactly the same feats
    pos_feats_parts = n.pos_feats.split(":")
    feats_from_pos_feats = pos_feats_parts[1:] if len(pos_feats_parts) > 1 else []
    feats_from_node = list(n.feats.values())
    if len(feats_from_pos_feats) != len(feats_from_node):
        # Rebuild pos_feats using the POS and the feats from the node
        n.pos_feats = n.pos + ":" + ":".join(feats_from_node)

    # Print warnings for any feats not in feats_dict
    test_feats(feats_from_node)

    # If feats is empty, check if pos_feats equals pos
    if not n.feats and n.pos_feats != n.pos:
        print(f"POS_FEATS {n.pos_feats} is not equal to POS {n.pos}.")

    # Test if feats_pos_combination is valid
    test_feats_pos_combination(n.pos, feats_from_node)

def process_conll_file(file_path: str, output_dir: str):
    """Reads a CONLL file, corrects each line, and writes the corrected file to output_dir with the same file name."""
    print(f"Processing file: {file_path}")
    corrected_lines = []
    with open(file_path, "r", encoding="utf-8") as infile:
        for line in infile:
            if line.strip() == "":
                corrected_lines.append("\n")
                continue
            n = Node(line)
            correct_conll_line(n)
            corrected_lines.append(str(n) + "\n")

    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(corrected_lines)
    print(f"Corrected file saved as: {output_path}")


def main():
    """Main function."""
    input_directory = input("Enter the path to the directory containing original CONLL files: ").strip()
    output_directory = input("Enter the path to the directory for output files: ").strip()

    if not os.path.isdir(input_directory):
        print("Input directory does not exist.")
        return

    if not os.path.isdir(output_directory):
        print("Output directory does not exist.")
        return

    for file in os.listdir(input_directory):
        if file.endswith(".conll"):
            file_path = os.path.join(input_directory, file)
            process_conll_file(file_path, output_directory)


if __name__ == "__main__":
    main()
