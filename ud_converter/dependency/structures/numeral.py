"""
Module for the conversion of numeral phrases to Universal Dependencies format.

This module handles the conversion of various types of numeral phrases:
- Standard numeral phrases
- Coordinated numeral phrases
- Multiword expression numeral phrases
- Named entity numeral phrases

Each type requires specific structural transformations to conform to UD guidelines.
"""
import logging
from typing import Iterable
from utils.classes import Token
from dependency.labels import convert_label as cl

logger = logging.getLogger('ud_converter.dependency.structures.numeral')


def convert_numeral(s: Iterable['Token'] ) -> None:
    """
    Converts numeral phrases from MPDT format to UD format.
    
    This function identifies different types of numeral phrases and applies
    the appropriate conversion function based on the syntactic context.
    
    :param Sentence s: An iterable of Token objects representing a sentence
    """
    for t in s:
        if t.pos == 'num':
            if t.children_with_label('comp'):
                standard_numeral(t)
            elif (t.gov.upos == 'CCONJ' or t.gov.upos == 'PUNCT' and t.dep_label == 'conjunct') and t.gov.children_with_label('comp'):
                coordinated_numeral(t)
            elif t.rec_child_with_label_via_label('mwe', 'comp'):
                mwe_numeral(t)
            elif t.rec_child_with_label_via_label('ne', 'comp'):
                ne_numeral(t)
            else:
                logger.warning('No conversion for numeral phrase: %s', t.form)


def standard_numeral(t: Token) -> None:
    """
    Converts standard numeral phrases to UD format.
    
    In standard numeral phrases, the complement becomes the head in UD,
    and the numeral becomes a modifier of the complement.
    
    :param Token t: The numeral Token to convert
    """
    comp = t.children_with_label('comp')
    if len(comp) != 1:
        logger.warning('Expected 1 comp child, got %d for standard numeral phrase: %s', len(comp), t.form)
        return
    comp : Token = comp[0]
    comp.ugov = t.gov
    comp.udep_label = '_'
    t.ugov = comp
    t.udep_label = numeral_label(t)
    for c in t.children:
        if c != comp and c.dep_label not in ['mwe', 'adjunct_compar']:
            if (c.lemma in ['ani', 'aż', 'blisko', 'bodaj', 'co', 'dopiero', 'jedynie', 'jeszcze', 'chociaż', 'coraz', 'jak',
                            'już', 'najwyżej', 'naprawdę', 'nawet', 'niemal', 'niespełna', 'około', 'ponad', 'prawie', 'przeszło', 
                            'przynajmniej', 'raptem', 'tak', 'tylko', 'z', 'za', 'zaledwie', 'zapewne', 'zbyt', 'znacznie'] 
            and c.upos in ['PART', 'X'] and c.dep_label in ['adjunct', 'adjunct_emph']):
                pass
            elif (c.lemma in ['jakiś', 'jaki', 'ten', 'wszystek'] and c.upos == 'DET' and c.dep_label == 'adjunct'):
                pass
            else:
                c.ugov = comp
                c.udep_label = cl(c)
        else:
            logger.warning('No label for standard numeral phrase: %s, %s', t.form, t.upos)


def coordinated_numeral(t: Token) -> None:
    """
    Converts coordinated numeral phrases to UD format.
    
    In coordinated numeral phrases, the complement becomes the head,
    and the coordination structure is reattached to the complement.
    
    :param Token t: The numeral Token to convert
    """
    comp = t.children_with_label('comp')
    if len(comp) != 1:
        logger.warning('Expected 1 comp child, got %d for coordinated numeral phrase: %s', len(comp), t.form)
        return
    comp = comp[0]
    comp.ugov = t.gov.gov
    comp.udep_label = cl(t.gov)
    t.gov.ugov = comp
    t.gov.udep_label = numeral_label(t.gov)


def mwe_numeral(t: Token) -> None:
    """
    Converts multiword expression numeral phrases to UD format.
    
    In MWE numeral phrases, the multiword expression becomes the head,
    and the numeral becomes a modifier of the MWE.
    
    :param Token t: The numeral Token to convert
    """
    mwe = t.rec_child_with_label_via_label('mwe', 'comp')
    mwe.ugov = t.gov
    mwe.udep_label = cl(t)
    t.ugov = mwe
    t.udep_label = numeral_label(t)


def ne_numeral(t: Token) -> None:
    """
    Converts named entity numeral phrases to UD format.
    
    In named entity numeral phrases, the named entity becomes the head,
    and the numeral becomes a flat modifier of the named entity.
    
    :param Token t: The numeral Token to convert
    """
    ne = t.children_with_label('ne')
    if ne != t.rec_child_with_label_via_label('ne', 'comp'):
        logger.warning('HERE WE PROBABLY HAVE A PROBLEM')
    if len(ne) != 1:
        logger.warning('Expected 1 named entity child, got %d for numeral phrase: %s', len(ne), t.form)
        return
    ne = ne[0]
    ne.ugov = t.gov
    ne.udep_label = cl(t)
    t.ugov = ne
    t.udep_label = 'nummod:flat'


def numeral_label(t: Token) -> str:
    """
    Determines the appropriate UD dependency label for a numeral token.
    
    :param Token t: The numeral Token to label
    :return: The appropriate UD dependency label ('nummod' for NUM, 'det' for DET)
    :rtype: str
    """
    if not t.udep_label and t.upos == 'NUM':
        return 'nummod'
    elif not t.udep_label and t.upos == 'DET':
        return 'det'
    else:
        logger.warning('No label for numeral phrase: %s, %s', t.form, t.upos)
        return '_'
