"""
Module for the lemma_based_upos function to be done before the POS-specific conversion.
"""
import re
import logging
from utils.classes import Token
from morphosyntax.conversion import pos_specific_upos

re_roman = re.compile(r'^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$')
re_arabic = re.compile(r'^\d+([\.,]\d+)*$')

logger = logging.getLogger('ud_converter.morphosyntax.preconversion')


def lemma_based_upos(t: Token) -> None:
    """
    Applies the lemma-based conversion.
    """
    if (t.lemma in ['niż', 'niżeli', 'anizeli', 'niźli', 'jakby', 'jakoby', 'niczym', 'niby'] and
    t.pos not in ['subst', 'part', 'adv']):
        t.upos = 'SCONJ'
        t.ufeats = {'ConjType': 'Comp'}
        logger.debug("Converted %s to %s", t.form, t.upos)
    elif t.lemma == 'jak' and t.pos not in ['subst', 'conj', 'adv']:
        t.upos = 'SCONJ'
        t.ufeats = {'ConjType': 'Comp'}
    elif t.lemma == 'temu':
        t.upos = 'ADP'
        t.ufeats = {'AdpType': 'Post', 'Case': 'Acc'}
        logger.debug("Converted %s to %s", t.form, t.upos)
    elif t.lemma in ['plus', 'minus'] and t.pos not in ['subst', 'part']:
        t.upos = 'CCONJ'
        t.ufeats = {'ConjType': 'Oper'}
        logger.debug("Converted %s to %s", t.form, t.upos)
    elif t.pos not in ['subst', 'ign'] and re_arabic.match(t.lemma):
        number(t)
        logger.debug("Converted %s to %s", t.form, t.upos)
    elif t.pos not in ['interj', 'qub', 'part', 'conj', 'ign', 'brev', 'subst', 'prep', 'xxs', 'xxx'] and re_roman.match(t.lemma):
        number(t, roman=True)
        logger.debug("Converted %s to %s", t.form, t.upos)
    elif t.lemma[0].isupper():
        pos_specific_upos(t)
        if t.pos in ['subst', 'depr']:
            t.upos = 'PROPN'
            logger.debug("Converted %s to %s", t.form, t.upos)

def number(t: Token, roman: bool = False) -> None:
    """Converts a number."""
    if t.upos == '':
        if t.pos == 'adj':
            pos_specific_upos(t)
            t.upos = 'ADJ'
            t.ufeats = {'NumType': 'Ord'}
        elif t.pos == 'num':
            pos_specific_upos(t)
            t.upos = 'NUM'
            t.ufeats = {'NumType': 'Card'}
        elif t.pos in ['dig', 'romandig', 'xxx']:
            t.upos = 'X'
        else:
            logger.warning('Unrecognised part of speech >>%s<< of the numeral >>%s<< in >>%s<<', t.pos, t.lemma, t.sentence.text if t.sentence else 'unknown')

    if roman is True:
        t.ufeats = {'NumForm': 'Roman'}
    else:
        t.ufeats = {'NumForm': 'Digit'}
