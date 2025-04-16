"""
Module for the lemma_based_upos function to be done before the POS-specific conversion.

This module handles pre-conversion rules that are based on the lemma rather than
the part of speech. It includes special handling for certain conjunctions, adpositions,
numbers, and capitalized words.
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
    Applies the lemma-based conversion to Universal POS tags.

    This function handles special cases where the UPOS tag depends on the lemma
    rather than just the part of speech. It includes handling for subordinating
    conjunctions, postpositions, coordinating conjunctions, numbers, and proper nouns.

    :param Token t: The token to be converted
    """
    if (t.lemma in ['niż', 'niżeli', 'anizeli', 'niźli', 'jakby', 'jakoby', 'niczym', 'niby'] and
    t.pos not in ['subst', 'part', 'adv']):
        t.upos = 'SCONJ'
        t.ufeats = {'ConjType': 'Comp'}
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
    elif t.lemma == 'jak' and t.pos not in ['subst', 'conj', 'adv']:
        t.upos = 'SCONJ'
        t.ufeats = {'ConjType': 'Comp'}
    elif t.lemma == 'temu':
        t.upos = 'ADP'
        t.ufeats = {'AdpType': 'Post', 'Case': 'Acc'}
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
    elif t.lemma in ['plus', 'minus'] and t.pos not in ['subst', 'part']:
        t.upos = 'CCONJ'
        t.ufeats = {'ConjType': 'Oper'}
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
    elif t.pos not in ['subst', 'ign'] and re_arabic.match(t.lemma):
        number(t)
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
    elif t.pos not in ['interj', 'qub', 'part', 'conj', 'ign', 'brev', 'subst', 'prep', 'xxs', 'xxx'] and re_roman.match(t.lemma):
        number(t, roman=True)
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
    elif t.lemma[0].isupper():
        pos_specific_upos(t)
        if t.pos in ['subst', 'depr']:
            t.upos = 'PROPN'
            logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)

def number(t: Token, roman: bool = False) -> None:
    """
    Converts a token that represents a number to the appropriate UPOS tag.

    This function handles various kinds of numerals, including ordinal numbers,
    cardinal numbers, and numbers written in digit or Roman numeral form.

    :param Token t: The token to be converted
    :param bool roman: Boolean flag indicating if the number is in Roman numeral format
    """
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
            logger.warning('Sentence %s: Unrecognised part of speech >>%s<< of the numeral >>%s<< in >>%s<<', t.sentence.id, t.pos, t.lemma, t.sentence.text if t.sentence else 'unknown')

    if roman is True:
        t.ufeats = {'NumForm': 'Roman'}
    else:
        t.ufeats = {'NumForm': 'Digit'}
