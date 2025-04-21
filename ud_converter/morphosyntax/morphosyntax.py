"""
Main module of ud_converter.morphosyntax package, responsible for the conversion of tokens to UPOS.

This module orchestrates the conversion process through three steps:
1. Preconversion - Initial conversion based on lexical properties
2. Core conversion - POS-specific conversion rules
3. Postconversion - Final adjustments and sentence-level conversions
"""
from utils.classes import Sentence
from morphosyntax.preconversion import lemma_based_upos as preconversion
from morphosyntax.conversion import pos_specific_upos as conversion
from morphosyntax.postconversion import post_conversion as postconversion


def convert_to_upos(s: Sentence, meta: dict[str, str]) -> None:
    """
    Converts tokens in a sentence to UPOS tags and features.

    This function processes all tokens in the given sentence through the complete
    conversion pipeline: preconversion, core conversion, and postconversion stages.

    :param Sentence s: The sentence containing tokens to be converted
    :param meta: Metadata dictionary with additional information for the conversion
    """
    for token in s.tokens:
        preconversion(token)
        conversion(token)
    postconversion(s, meta)
