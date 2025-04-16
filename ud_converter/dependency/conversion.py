"""
Module for the conversion of dependency structures from MPDT to UD format.

This module handles the complete pipeline for converting dependency structures,
including preprocessing, structural conversions, and label mapping according to
Universal Dependencies guidelines.
"""
from utils.classes import Sentence
from dependency.preconversion import preconversion
from dependency.structures.numeral import convert_numeral
from dependency.structures.prepositional import convert_prepositional
from dependency.structures.copula import convert_copula
from dependency.structures.subordination import convert_subordination
from dependency.structures.coordination import convert_coordination
from dependency.labels import convert_label as label_conversion
from dependency.edges import edges_correction
from dependency.postconversion import postconversion


def main(s: Sentence) -> None:
    """
    Main function for the conversion of dependencies to Universal Dependencies format.
    
    This function orchestrates the complete dependency conversion pipeline,
    including preconversion, structure conversion, and label conversion.
    
    :param Sentence s: The sentence to convert
    """
    preconversion(s)
    structure_conversion(s)
    for t in s.tokens:
        label_conversion(t)
    edges_correction(s)
    postconversion(s)


def structure_conversion(s: Sentence) -> None:
    """
    Converts the sentence structure according to Universal Dependencies guidelines.
    
    This function applies a series of structure transformations to convert
    specific syntactic constructions, including numerals, prepositional phrases,
    copula constructions, subordinate clauses, and coordination structures.
    
    :param Sentence s: The sentence to convert
    """
    convert_numeral(s)
    convert_prepositional(s)
    convert_copula(s)
    convert_subordination(s)
    convert_coordination(s)
