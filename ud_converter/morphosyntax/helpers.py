"""
Module for helper functions supporting morphosyntactic conversion.

This module provides utility functions specifically for the morphosyntax module,
particularly for handling gender, number, and other morphological features during
the conversion from MPDT to Universal Dependencies format.
"""
import logging
from utils.classes import Token
from utils.constants import FEATS_UPDATE as FU

logger = logging.getLogger('ud_converter.morphosyntax.helpers')


def update_gender_number(t: Token) -> None:
    """
    Updates the gender and number features of a token to UD format.

    This function maps Middle Polish gender and number features to their Universal
    Dependencies equivalents. It handles special cases such as:
    - Masculine animate vs inanimate distinctions
    - Pluralia tantum nouns
    - Gender-specific number agreement

    :param Token t: The token whose gender and number features to update
    """
    gender = t.feats.get('gender', None)
    number = t.feats['number']
    if gender == 'manim1':
        t.ufeats = {'Gender': 'Masc', 'Animacy': 'Hum', 'Number': FU[number]}
    elif gender == 'manim2':
        t.ufeats = {'Gender': 'Masc', 'Animacy': 'Nhum', 'Number': FU[number]}
    elif gender == 'm':
        t.ufeats = {'Gender': 'Masc', 'Number': FU[number]}
    elif gender == 'f':
        t.ufeats = {'Gender': 'Fem', 'Number': FU[number]}
    elif gender == 'n':
        t.ufeats = {'Gender': 'Neut', 'Number': FU[number]}
    else:
        logger.warning("S%-5s T%-5s- Unknown gender: '%s' in token '%s' with pos '%s'", t.sentence.id, t.id, gender, t.form, t.pos)
    if t.feats.get('subgender', None) == 'pt':
        t.ufeats = {'Number': 'Ptan'}
