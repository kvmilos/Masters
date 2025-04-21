"""
Module for the conversion of numeral phrases to Universal Dependencies format.

This module handles the conversion of various types of numeral phrases:
- Standard numeral phrases
- Coordinated numeral phrases
- Multiword expression numeral phrases
- Named entity numeral phrases

Each type requires specific structural transformations to conform to UD guidelines.
"""
from utils.logger import ChangeCollector
from utils.classes import Sentence, Token
from dependency.labels import convert_label as cl


def convert_numeral(s: Sentence) -> None:
    """
    Converts numeral phrases from MPDT format to UD format.

    This function identifies different types of numeral phrases and applies
    the appropriate conversion function based on the syntactic context.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        if t.pos == 'num':
            if t.children_with_label('comp'):
                standard_numeral(t)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted standard numeral phrase: '{t.form}'", module="structures.numeral")
            elif t.gov and (t.gov.upos == 'CCONJ' or t.gov.upos == 'PUNCT' and t.dep_label == 'conjunct') and t.gov.children_with_label('comp'):
                coordinated_numeral(t)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted coordinated numeral phrase: '{t.form}'", module="structures.numeral")
            elif t.super_child_with_label_via_label('mwe', 'comp'):
                mwe_numeral(t)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted MWE numeral phrase: '{t.form}'", module="structures.numeral")
            elif t.super_child_with_label_via_label('ne', 'comp'):
                ne_numeral(t)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted NE numeral phrase: '{t.form}'", module="structures.numeral")
            else:
                ChangeCollector.record(t.sentence.id, t.id, f"No conversion for numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')


def standard_numeral(t: Token) -> None:
    """
    Converts standard numeral phrases to UD format.

    In standard numeral phrases, the complement becomes the head in UD,
    and the numeral becomes a modifier of the complement.

    :param Token t: The numeral Token to convert
    """
    comp = t.children_with_label('comp')
    if len(comp) != 1:
        ChangeCollector.record(t.sentence.id, t.id, f"Expected 1 comp child, got {len(comp)} for standard numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')
        return
    comp_t = comp[0]
    if t.gov:
        comp_t.ugov = t.gov
        comp_t.udep_label = '_'
    t.ugov = comp_t
    t.udep_label = numeral_label(t)
    for c in t.children:
        if c != comp and c.dep_label not in ['mwe', 'adjunct_compar']:
            if (
                c.lemma in [
                    'ani', 'aż', 'blisko', 'bodaj', 'co', 'dopiero', 'jedynie', 'jeszcze', 'chociaż', 'coraz', 'jak',
                    'już', 'najwyżej', 'naprawdę', 'nawet', 'niemal', 'niespełna', 'około', 'ponad', 'prawie', 'przeszło',
                    'przynajmniej', 'raptem', 'tak', 'tylko', 'z', 'za', 'zaledwie', 'zapewne', 'zbyt', 'znacznie'
                ]
                and c.upos in ['PART', 'X']
                and c.dep_label in ['adjunct', 'adjunct_emph']
            ):
                pass
            elif (c.lemma in ['jakiś', 'jaki', 'ten', 'wszystek'] and c.upos == 'DET' and c.dep_label == 'adjunct'):
                pass
            else:
                c.ugov = comp_t
                c.udep_label = cl(c)


def coordinated_numeral(t: Token) -> None:
    """
    Converts coordinated numeral phrases to UD format.

    In coordinated numeral phrases, the complement becomes the head,
    and the coordination structure is reattached to the complement.

    :param Token t: The numeral Token to convert
    """
    comp = t.children_with_label('comp')
    if len(comp) != 1:
        ChangeCollector.record(t.sentence.id, t.id, f"Expected 1 comp child, got {len(comp)} for coordinated numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')
        return
    comp_t = comp[0]
    if t.gov and t.gov.gov:
        comp_t.ugov = t.gov.gov
        comp_t.udep_label = cl(t.gov)
        t.gov.ugov = comp_t
        t.gov.udep_label = numeral_label(t.gov)
    else:
        ChangeCollector.record(t.sentence.id, t.id, f"No governor for coordinated numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')


def mwe_numeral(t: Token) -> None:
    """
    Converts multiword expression numeral phrases to UD format.

    In MWE numeral phrases, the multiword expression becomes the head,
    and the numeral becomes a modifier of the MWE.

    :param Token t: The numeral Token to convert
    """
    mwe = t.super_child_with_label_via_label('mwe', 'comp')
    if t.gov and mwe:
        mwe.ugov = t.gov
        mwe.udep_label = cl(t)
    if not mwe:
        ChangeCollector.record(t.sentence.id, t.id, f"No MWE found for numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')
        return
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
    if ne != t.super_child_with_label_via_label('ne', 'comp'):
        ChangeCollector.record(t.sentence.id, t.id, "HERE WE PROBABLY HAVE A PROBLEM", module="structures.numeral", level='WARNING')
    if len(ne) != 1:
        ChangeCollector.record(t.sentence.id, t.id, f"Expected 1 named entity child, got {len(ne)} for numeral phrase: '{t.form}'", module="structures.numeral", level='WARNING')
        return
    ne_t = ne[0]
    if t.gov:
        ne_t.ugov = t.gov
        ne_t.udep_label = cl(t)
    t.ugov = ne_t
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
        ChangeCollector.record(t.sentence.id, t.id, f"No label for numeral phrase: '{t.form}', {t.upos}", module="structures.numeral", level='WARNING')
        return '_'
