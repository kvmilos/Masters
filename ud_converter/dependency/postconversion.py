"""
Module for handling enhanced Universal Dependencies.

This module provides functions for completing enhanced dependency graphs
according to Universal Dependencies guidelines.
"""
import logging
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.dependency.postconversion')


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

    This function modifies the ufeats dictionary to distinguish between
    interrogative and relative pronouns based on their syntactic context.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.upos == 'PRON' and 'PronType' in t.ufeats and t.ufeats['PronType'] == 'Int,Rel':
            pronoun_type = look_for_clause_type(t)
            if pronoun_type == 'Rel':
                t.ufeats['PronType'] = 'Rel'
            elif pronoun_type == 'Int':
                t.ufeats['PronType'] = 'Int'
            elif pronoun_type == 'Mwe':
                t.ufeats.pop('PronType', None)


def look_for_clause_type(t: Token) -> str:
    """
    Determines the clause type for a pronoun based on its syntactic context.

    This function recursively examines the dependency path to determine
    whether a pronoun is used in a relative clause, an interrogative clause,
    a multiword expression, or as a root.

    :param Token t: The pronoun token
    :return: The clause type ('Rel', 'Int', 'Mwe', or '')
    :rtype: str
    """
    gov = t.ugov
    if gov:
        if t.udep_label == 'acl:relcl':
            return 'Rel'
        if t.udep_label.startswith('ccomp') or t.udep_label.startswith('xcomp') or t.udep_label.startswith('advcl') or t.udep_label == 'root':
            return 'Int'
        if t.udep_label == 'fixed':
            return 'Mwe'
        return look_for_clause_type(gov)
    else:
        logger.warning('No governor found for pronoun: %s', t.form)
        return ''
