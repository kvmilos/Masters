"""
Module for handling enhanced Universal Dependencies.

This module provides functions for completing enhanced dependency graphs
according to Universal Dependencies guidelines.
"""
from utils.classes import Sentence


def postconversion(s: Sentence) -> None:
    """
    Orchestrates the post-conversion process for a sentence.

    This function applies various post-conversion steps to ensure the
    enhanced dependency graph is correctly completed.

    :param Sentence s: The sentence to process
    """
    pronouns_disambiguation(s)
    default_label_conversion(s)
    complete_eud(s)


def complete_eud(s: Sentence) -> None:
    """
    Completes the enhanced dependency graph for a sentence.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.ugov:
            # Add the basic dependency to the enhanced dependencies
            t.eud = {t.ugov.id: t.udep_label}

            # Handle special cases for mark_rel
            if t.udep_label == 'mark_rel':
                t.udep_label = 'mark'
                if t.ugov.gov:
                    t.eud = {t.ugov.gov.id: 'ref'}

        # Update any placeholder labels
        for gov, label in list(t.eud.items()):
            if label == '_' and t.ugov:
                t.eud = {gov: t.ugov.udep_label}


def default_label_conversion(s: Sentence) -> None:
    """
    Applies default label conversions for any remaining unconverted labels.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.udep_label == '_':
            if t.dep_label == 'conjunct':
                t.udep_label = 'case' if t.upos == 'ADP' else 'conj'
            else:
                t.udep_label = 'dep'


def pronouns_disambiguation(s: Sentence) -> None:
    """
    Disambiguates pronouns in the sentence.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.upos == 'PRON' and 'PronType' in t.ufeats and t.ufeats['PronType'] == 'Int,Rel':
            # ... TODO
