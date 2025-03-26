"""
Main module for converting dependency trees from CoNLL-X to UD CONLL-U.
Usage:
    python converter.py input_file.conll output_file.conllu [meta_file.json] [--tags-only]

--tags-only: if present, only performs POS -> UPOS conversion.
Full dependency conversion is not implemented.
"""

import sys

from utils.io import read_conll, write_ud_conll, load_meta
from utils.logger import setup_logging
from morphosyntax.conversion import convert_to_upos

logger = setup_logging()


def main():
    """
    Main function for the converter.
    """
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} input_file.conll output_file.conllu [meta_file.json] [--tags-only]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    meta_file = None
    tags_only = False

    for arg in sys.argv[3:]:
        if arg == "--tags-only":
            tags_only = True
        elif arg.endswith(".json"):
            meta_file = arg

    meta_data = load_meta(meta_file) if meta_file else None

    logger.info("Reading input file %s", input_file)
    sentences = read_conll(input_file)
    logger.info("Read %d sentences", len(sentences))

    if tags_only:
        logger.info("Performing tags-only conversion.")
    else:
        logger.info("Performing full dependency conversion.")

    for sentence in sentences:
        convert_to_upos(sentence)

    logger.info("Writing output to %s", output_file)
    write_ud_conll(sentences, output_file, meta_data)
    logger.info("Conversion completed.")

if __name__ == '__main__':
    main()
