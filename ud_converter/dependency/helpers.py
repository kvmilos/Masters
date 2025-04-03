"""
Module for helpers specific to the dependency module.
"""
import logging
from utils.classes import Token
logger = logging.getLogger('ud_converter.dependency.helpers')


def convert_label(t: Token) -> str:
    """
    Converts the dependency label to the UD format and returns it.
    """
    if t.udep_label != '_':
        return t.udep_label

    if t.pos == 'sym' and t.dep_label == 'adjunct_comment':
        return 'discourse'
    elif t.pos == 'interj' and t.dep_label != 'root':
        return 'discourse:intj'
    elif t.lemma == 'o' and t.children_with_lemma('tyle') == 1 and t.children_with_lemma('tyle')[0].dep_label == 'mwe':
        return 'mark'
    elif t.lemma == 'o' and t.children_with_lemma('tyle') > 1:
        logger.warning('Multiple "tyle"-lemma children for o: %s', t.form)
    elif t.upos == 'DET' and t.pos != 'num' and t.dep_label in ['adjunct', 'poss']:
        if t.ufeats['Poss'] == 'Yes':
            return 'det:poss'
        else:
            return 'det'
