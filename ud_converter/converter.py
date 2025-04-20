"""
Main module for converting dependency trees from CoNLL-X to UD CONLL-U.

This module provides the primary entry point for the MPDT to UD conversion tool.
It handles command-line arguments, coordinates the conversion pipeline,
and manages I/O operations.

Usage:
    python converter.py input_file.conll output_file.conllu [meta_file.json] [--tags-only]

--tags-only: if present, only performs POS -> UPOS conversion.
"""
import sys
import logging
from collections import defaultdict
from utils.io import read_conll, write_ud_conll, load_meta
from utils.logger import setup_logging, ChangeCollector
from morphosyntax.morphosyntax import convert_to_upos
from dependency.conversion import main as convert_dependencies

setup_logging()
logger = logging.getLogger('ud_converter')


def main() -> None:
    """
    Main function for the converter.

    Processes command-line arguments, reads input files, performs the conversion,
    and writes the results to the specified output file. Supports both full
    conversion and tags-only mode.
    """
    if len(sys.argv) < 3:
        print(f'Usage: python {sys.argv[0]} input_file.conll output_file.conllu [meta_file.json] [--tags-only]')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    meta_file = None
    tags_only = False
    form = 'ud'

    for arg in sys.argv[3:]:
        if arg == '--tags-only':
            tags_only = True
            form = 'ud-tags-only'

        elif arg.endswith('.json'):
            meta_file = arg

    meta_data = load_meta(meta_file) if meta_file else {}

    logger.info('Reading input file %s', input_file)
    sentences = read_conll(input_file, meta_data)
    logger.info('Read %d sentences', len(sentences))

    if tags_only:
        logger.info('Performing tags-feats-only conversion.')
        for sentence in sentences:
            convert_to_upos(sentence, sentence.meta)
    else:
        logger.info('Performing full dependency conversion.')
        logger.info('Converting tags and feats.')
        for sentence in sentences:
            convert_to_upos(sentence, sentence.meta)
        logger.info('Converting dependencies.')
        for sentence in sentences:
            # clear previous events for this sentence
            ChangeCollector.clear()
            convert_dependencies(sentence)
            # group events by token id and log in token order
            events_by_token = defaultdict(list)
            for _, tid, msg in ChangeCollector.get_events():
                events_by_token[tid].append(msg)
            # log with padded prefix S<sid>T<tid>:
            for token in sentence.tokens:
                tid = token.id
                if tid in events_by_token:
                    for msg in events_by_token[tid]:
                        logger.debug("S%-5s T%-5s- %s", sentence.id, tid, msg)
            ChangeCollector.clear()

    logger.info('Writing output to %s', output_file)
    write_ud_conll(sentences, output_file, meta_data, form)
    logger.info('Conversion completed.')

if __name__ == '__main__':
    main()
