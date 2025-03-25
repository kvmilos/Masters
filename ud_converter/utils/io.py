"""
Module for reading and writing CONLL files.
"""
from utils.classes import Sentence, Token

def read_conll(filepath):
    """
    Reads a .conll file and returns a list of Sentence objects.
    Blank lines separate sentences.
    Lines starting with '#' (if any) are treated as comments and are skipped.
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
