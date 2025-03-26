"""
Module for reading and writing CONLL files.
"""
import logging
import json
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.io')

def read_conll(filepath):
    """
    Reads a .conll file and returns a list of Sentence objects.
    Blank lines separate sentences.
    Lines starting with '#' (if any) are treated as comments and skipped.
    """
    sentences = []
    current_lines = []

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('#'):
                continue
            if line.strip() == '':
                if current_lines:
                    tokens = [Token(l) for l in current_lines]
                    sentence = Sentence(tokens)
                    sentences.append(sentence)
                    current_lines = []
            else:
                current_lines.append(line)
        if current_lines:
            tokens = [Token(l) for l in current_lines]
            sentence = Sentence(tokens)
            sentences.append(sentence)

    return sentences

def write_ud_conll(sentences, outfile_path, meta=None):
    """
    Writes the converted sentences in UD CONLL-U format to outfile_path.
    For each sentence, writes metadata lines (if available) then each token by calling its __str__.
    """
    with open(outfile_path, 'w', encoding='utf-8') as out:
        for idx, sentence in enumerate(sentences, start=1):
            if meta and str(idx) in meta:
                sent_meta = meta[str(idx)]
                if 'sent_id' in sent_meta:
                    out.write(f"# sent_id = {sent_meta['sent_id']}\n")
                if 'text' in sent_meta:
                    out.write(f"# text = {sent_meta['text']}\n")
            else:
                out.write(f"# sent_id = {idx}\n")
                out.write(f"# text = {sentence.text}\n")
            out.write(str(sentence))
            out.write("\n")


def load_meta(meta_path: str) -> dict:
    """
    Loads metadata from a JSON file.
    """
    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning("Could not load metadata from %s: %s", meta_path, e, exc_info=True)
        return {}
