"""
Module for the conversion of the sentence.
"""
from utils.classes import Sentence
from dependency.preconversion import preconversion
from dependency.structures.numeral import convert_numeral
from dependency.structures.prepositional import convert_prepositional
from dependency.structures.copula import convert_copula
from dependency.structures.subordination import convert_subordination
from dependency.structures.coordination import convert_coordination


def main(s: Sentence) -> None:
    """
    Main function for the conversion of dependencies to UD.
    """
    preconversion(s)
    structure_conversion(s)
    label_conversion(s)


def structure_conversion(s: Sentence) -> None:
    """
    Conversion of the sentence structure.
    """
    convert_numeral(s)
    convert_prepositional(s)
    convert_copula(s)
    convert_subordination(s)
    convert_coordination(s)


def label_conversion(s: Sentence) -> None:
    """
    Conversion of the dependency labels.
    """
    ...
