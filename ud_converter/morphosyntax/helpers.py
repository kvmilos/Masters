"""
Module for helpers specific to the morphosyntax module.
"""

import logging
from utils.classes import Token
from utils.feats_dict import FEATS_UPDATE as FU

logger = logging.getLogger('ud_converter.morphosyntax.helpers')

def update_gender_number(t: Token):
    """
    Updates the gender and number of the token.
    :param token: current token
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
    elif gender == 'f':
        t.ufeats = {'Gender': 'Fem', 'Number': FU[number]}
    elif gender == 'n':
        t.ufeats = {'Gender': 'Neut', 'Number': FU[number]}
    elif gender == 'p1':
        t.ufeats = {'Gender': 'Masc', 'Animacy': 'Hum', 'Number': 'Ptan'}
    elif gender == 'p2':
        t.ufeats = {'Gender': 'Neut', 'Number': 'Ptan'}
    else:
        logger.warning('Unknown gender: %s', gender)
