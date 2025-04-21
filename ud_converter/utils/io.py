"""
Module for reading and writing CoNLL files.

This module provides functions for reading CoNLL files and writing
CONLL-U files in the Universal Dependencies format, as well as
loading metadata from JSON files.
"""
import logging
import json
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.io')


def read_conll(filepath: str, meta: dict[str, dict[str, str]] | None = None) -> list[Sentence]:
    """
    Reads a .conll file and returns a list of Sentence objects.

    Blank lines separate sentences. Lines starting with '#' (if any)
    are treated as comments and skipped.

    :param str filepath: Path to the CoNLL-X format file to read
    :param meta: Optional dictionary of metadata keyed by sentence index
    :return: List of Sentence objects containing the parsed sentences
    :rtype: List[Sentence]
    """
    sentences: list[Sentence] = []
    current_lines: list[str] = []
    sent_count = 0

    with open(filepath, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('#'):
                continue
            if line.strip() == '':
                if current_lines:
                    sent_count += 1
                    tokens = [Token(cur_line) for cur_line in current_lines]
                    sentence = Sentence(tokens)
                    if meta:
                        sent_meta = meta.get(str(sent_count), {'sent_id': str(sent_count)})
                        sentence.meta = sent_meta
                    sentences.append(sentence)
                    current_lines = []
            else:
                current_lines.append(line)
        if current_lines:
            sent_count += 1
            tokens = [Token(cur_line) for cur_line in current_lines]
            sentence = Sentence(tokens)
            if meta:
                sent_meta = meta.get(str(sent_count), {'sent_id': str(sent_count)})
                sentence.meta = sent_meta
            sentences.append(sentence)

    return sentences


def write_ud_conll(sentences: list[Sentence], outfile_path: str, meta: dict[str, dict[str, str]] | None = None, form='ud') -> None:
    """
    Writes the converted sentences in UD CONLL-U format.

    For each sentence, writes metadata lines (if available) then each token
    by calling its to_string method.

    :param List[Sentence] sentences: List of Sentence objects to write
    :param str outfile_path: Path to the output file
    :param meta: Dictionary of metadata keyed by sentence index (as string)
    """
    with open(outfile_path, 'w', encoding='utf-8') as out:
        for idx, sentence in enumerate(sentences, start=1):
            # if exists, set metadata, if not None, set empty dict
            sent_meta = meta[str(idx)] if meta else {}
            sentence.meta = sent_meta
            sentence.write_meta(out)
            out.write(sentence.to_string(form))
            out.write("\n\n")


def load_meta(meta_path: str):
    """
    Loads metadata from a JSON file.

    :param meta_path: Path to the JSON metadata file
    :return: Dictionary containing the metadata
    """
    try:
        with open(meta_path, encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning('Could not load metadata from %s: %s', meta_path, e, exc_info=True)
        return {}
