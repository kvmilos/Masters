"""
Main module of ud_converter.morphosyntax package, responsible for the conversion of tokens to UPOS.
"""

from utils.classes import Token
from morphosyntax.preconversion import lemma_based_upos
from morphosyntax.conversion import pos_specific_upos

def convert_to_upos(t: Token):
    """
    Converts the token to UPOS.
    """
    lemma_based_upos(t)
    pos_specific_upos(t)
