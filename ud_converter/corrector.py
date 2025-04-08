"""
Corrector for MPDT CoNLL files.

This script corrects MPDT CoNLL file(s). It can be run with a single file
or a directory containing multiple files. If the "--test" argument is provided,
the script will run additional tests (using assertions) on the corrected lines.

Usage:
    python corrector.py <input_file_or_directory_path> <output_directory_path> [--test]

Example:
    python corrector.py data/MPDT_2000.conll data/corrected/
    python corrector.py data/original/ data/corrected/
    python corrector.py data/MPDT_2000.conll data/corrected/ --test (for that, you need to have tests/corrector_tests.py)
"""
import os
import sys
import re


def correct_gender_and_neut(line: str) -> str:
    """
    Applies corrections to the gender and accentability fields of the line.

    It replaces occurrences of 'zneut' with 'neut' and fixes n2 to n, and if ':m' appears in the POS features
    while '|n' is present in FEATS, it changes ':m' to ':n'.
    """
    fields = line.split('\t')
    if 'zneut' in fields[4] or 'zneut' in fields[5]:
        fields[4] = fields[4].replace('zneut', 'neut')
        fields[5] = fields[5].replace('zneut', 'neut')

    fields[4] = re.sub(r'\bn2\b', 'n', fields[4])
    fields[5] = re.sub(r'\bn2\b', 'n', fields[5])

    if (':m:' in fields[4] or ':m\t' in fields[4]) and ('|n|' in fields[5] or '|n\t' in fields[5]):
        fields[4] = fields[4].replace(':m:', ':n:')
        fields[4] = fields[4].replace(':m\t', ':n\t')

    return '\t'.join(fields)


def correct_conll_line_fields(line: str) -> str:
    """
    Corrects a single CONLL line by adjusting the POS and feature columns.

    The fields are assumed to be:
      0: ID, 1: FORM, 2: LEMMA, 3: POS, 4: POS_FEATS, 5: FEATS, etc.

    Corrections applied:
      - The correct_gender_and_neut function is applied.
      - The POS field (column 3) is trimmed to remove any extra appended features (using the first element).
      - The POS_FEATS field (column 4) is split by colon; the features (everything after the first element)
        are compared with the features obtained from the FEATS field (column 6, split by "|").
      - If their lengths differ, the POS_FEATS field is rebuilt as POS + ":" + ":".join(feats_from_token).
    """
    line = correct_gender_and_neut(line)

    fields = line.split('\t')
    # Adjust POS (field 3)
    if ':' in fields[3]:
        fields[3] = fields[3].split(":")[0]

    # Extract features from POS_FEATS (field 4)
    pos_feats_parts = fields[4].split(":")
    feats_from_pos_feats = pos_feats_parts[1:] if len(pos_feats_parts) > 1 else []

    # Extract features from FEATS (field 5); if "_" then no features.
    feats_from_token = [] if fields[5] == "_" else fields[5].split("|")

    if len(feats_from_pos_feats) != len(feats_from_token):
        fields[4] = fields[3] + (":" + ":".join(feats_from_token) if feats_from_token else "")

    return '\t'.join(fields)


def process_conll_file(file_path: str, output_dir: str, test: bool = False) -> None:
    """
    Reads a CONLL file from file_path, applies corrections to each non-empty line,
    and writes the corrected file to output_dir with the same filename.

    :param str file_path: Path to the input CONLL file
    :param str output_dir: Directory where corrected file will be saved
    :param bool test: If True, runs validation tests on the corrected lines
    """
    print(f'Processing file: {file_path}')
    corrected_lines = []
    with open(file_path, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.strip() == "":
                corrected_lines.append("\n")
                continue
            # Correct the line
            corrected_lines.append(correct_conll_line_fields(line))

    # If testing is enabled, run assertions on the corrected lines.
    if test:
        from tests.corrector_tests import test_pos, test_feats, test_feats_pos_combination
        test_pos(corrected_lines)
        test_feats(corrected_lines)
        test_feats_pos_combination(corrected_lines)

    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, file_name)
    with open(output_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(corrected_lines)
    print(f'Corrected file saved as: {output_path}')

def main() -> None:
    """Main function."""
    if len(sys.argv) not in {3, 4}:
        print('Usage: python corrector.py <input_file_or_directory_path> <output_directory_path> [--test]')
        return

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    test = len(sys.argv) == 4 and sys.argv[3] == '--test'

    if not os.path.exists(input_path):
        print(f'Input path {input_path} does not exist.')
        return

    os.makedirs(output_path, exist_ok=True)

    if os.path.isdir(input_path):
        for file in os.listdir(input_path):
            if file.endswith(".conll"):
                file_path = os.path.join(input_path, file)
                process_conll_file(file_path, output_path, test)
    else:
        process_conll_file(input_path, output_path, test)

if __name__ == "__main__":
    main()
