"""
Module for post-processing after the main tag conversion.

This module handles tasks that need to be performed after the main POS and feature
conversion, such as handling multiword expressions and space-after annotations.
"""
from utils.classes import Sentence, Token
from utils.logger import ChangeCollector


def post_conversion(s: Sentence, meta: dict[str, str]) -> None:
    """
    Handles post-processing tasks after the main tag conversion.

    This function orchestrates various post-conversion processes including
    multiword expression handling and space-after annotations.

    :param Sentence s: The sentence to process
    :param meta: Metadata dictionary with additional information for the conversion
    """
    text = meta.get("text")
    correction(s)
    add_mwe(s, text)
    add_no_space_misc(s, text)


def correction(s: Sentence) -> None:
    """
    Applies corrections to the sentence's tokens based on specific rules.

    This function checks for auxiliary verbs with 'aux' dep label and changes their UPOS tag from 'VERB' to 'AUX'.
    It also records the changes made for each token.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.upos == 'VERB' and t.dep_label == 'aux':
            old_upos = t.upos
            t.upos = 'AUX'
            ChangeCollector.record(t.sentence.id, t.id, f"upos changed from {old_upos} to {t.upos}", module="postconversion")


def add_mwe(s: Sentence, text: str | None) -> None:
    """
    Adds multiword tokens (MWEs) to the sentence.

    This function identifies multiword expressions based on the original text
    and creates special multiword tokens. The new multiword token is inserted
    at the beginning of the group in the sentence's token list.

    :param Sentence s: The sentence to process
    :param str text: The original text of the sentence
    """
    if not text:
        return

    new_tokens = []
    tokens = s.tokens
    pointer = 0
    i = 0
    while i < len(tokens):
        current_token = tokens[i]
        pos = text.find(current_token.form, pointer)
        if pos == -1:
            new_tokens.append(current_token)
            i += 1
            continue
        pointer = pos + len(current_token.form)
        group = [current_token]
        while i + 1 < len(tokens) and pointer < len(text):
            next_char = text[pointer]
            if next_char == ' ':
                break
            elif current_token.upos == 'PUNCT' or tokens[i + 1].upos not in ['AUX', 'PART'] and (tokens[i + 1].upos != 'PRON' or 'Variant' not in tokens[i + 1].ufeats or tokens[i + 1].ufeats['Variant'] != 'Short'):
                break
            i += 1
            next_token = tokens[i]
            group.append(next_token)
            pointer += len(next_token.form)
        if len(group) > 1:
            first = group[0]
            last = group[-1]
            mwe_token = Token('mwe')
            mwe_token.id = f'{first.id}-{last.id}'
            mwe_token.form = ''.join(t.form for t in group)
            mwe_token.umisc = {'Translit': ''.join(t.umisc.get('Translit', t.form) for t in group)}
            mwe_token.sentence = s
            new_tokens.append(mwe_token)
            new_tokens.extend(group)
        else:
            new_tokens.append(current_token)
        i += 1
    s.tokens = new_tokens
    s.dict_by_id = {token.id: token for token in new_tokens}


def add_no_space_misc(s: Sentence, text: str | None) -> None:
    """
    Adds SpaceAfter=No to UD misc for tokens that are not followed by a space.

    This function analyzes the original text to determine which tokens are not
    followed by spaces and marks them accordingly in the UD MISC field.

    :param Sentence s: The sentence to process
    :param str text: The original text of the sentence, if available
    """
    if not text:
        return

    excluded_ids = set()
    for token in s.tokens:
        if '-' in token.id:
            try:
                start_str, end_str = token.id.split('-')
                start = int(start_str)
                end = int(end_str)
                for num in range(start, end + 1):
                    excluded_ids.add(str(num))
            except Exception:
                pass

    new_tokens = [token for token in s.tokens if token.id not in excluded_ids]

    pointer = 0
    for i, token in enumerate(new_tokens):
        if '-' in token.id:
            continue

        token_form = token.form
        pos = text.find(token_form, pointer)
        if pos == -1:
            continue
        pointer = pos + len(token_form)
        if i == len(new_tokens) - 1:
            token.umisc.pop('SpaceAfter', None)
            continue
        if pointer >= len(text) or text[pointer] != " ":
            token.umisc['SpaceAfter'] = 'No'
        else:
            token.umisc.pop('SpaceAfter', None)
            pointer += 1
