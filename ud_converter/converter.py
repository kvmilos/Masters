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
            # Replay events in module grouping and token order from the sentence
            events = ChangeCollector.get_events()
            # map each token.id to its position in the sentence for ordering
            token_order = {tok.id: idx for idx, tok in enumerate(sentence.tokens)}
            # sort events by sentence ID (as int) then by token position
            events.sort(key=lambda e, to=token_order: (int(e[0]), to.get(e[1], float('inf'))))
            # replay sorted events
            for sid, tid, module, level, msg in events:
                mod = module or 'conversion'
                lg = logging.getLogger(f"ud_converter.dependency.{mod}")
                if level == 'DEBUG':
                    lg.debug("S%-5s T%-5s- %s", sid, tid, msg)
                else:
                    lg.warning("S%-5s T%-5s- %s", sid, tid, msg)
            # Clear events after replay
            ChangeCollector.clear()

    logger.info('Writing output to %s', output_file)
    write_ud_conll(sentences, output_file, meta_data, form)
    logger.info('Conversion completed.')

    # -------------------------------------------------------
    # to be deleted later
    logger.info('Creating second file with adequate changes.')
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() and not line.startswith('#'):
            fields = line.strip().split('\t')
            upos_feats = fields[4]  # 5th column
            morph_feats = fields[5]  # 6th column

            if any(upos_feats.startswith(prefix) for prefix in ('praet', 'ppas', 'pact')):
                morph_feats = morph_feats.replace('|Degree=Pos', '')
            morph_feats = morph_feats.replace('Number=Ptan', 'Number=Plur')

            fields[5] = morph_feats
            lines[i] = '\t'.join(fields) + '\n'

    with open(output_file.replace('.conllu', '-degree-number.conllu'), 'w', encoding='utf-8') as f:
        f.writelines(lines)

    logger.info('Wrote output to %s', output_file.replace('.conllu', '-degree-number.conllu'))
    # -------------------------------------------------------


if __name__ == '__main__':
    main()
