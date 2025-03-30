"""
Main module of ud_converter.morphosyntax package, responsible for the conversion of tokens to UPOS.
"""

from utils.classes import Sentence
from morphosyntax.preconversion import lemma_based_upos as preconversion
from morphosyntax.conversion import pos_specific_upos as conversion
from morphosyntax.postconversion import post_conversion as postconversion

def convert_to_upos(s: Sentence) -> None:
    """
    Converts the token to UPOS.
    """
    for token in s:
        preconversion(token)
        conversion(token)
        postconversion()
