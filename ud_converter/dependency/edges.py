"""
Module for handling edge corrections in the dependency graph.

This module provides functions for correcting dependency edges according to
Universal Dependencies guidelines, including:
1. Removing dependents from auxiliary verbs
2. Removing dependents from fixed expressions
3. Correcting flat structures to ensure left-to-right attachment
4. Removing dependents from mark, case, and cc nodes

These corrections ensure that the final dependency graph adheres to
Universal Dependencies constraints on which nodes can have dependents.
"""
import logging
from typing import List, Optional
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.dependency.edges')


def edges_correction(s: Sentence) -> None:
    """
    Applies edge corrections to the dependency graph.

    This function orchestrates the application of various edge correction
    rules to ensure the dependency graph adheres to Universal Dependencies
    guidelines.

    :param Sentence s: The sentence to process
    """
    remove_dependents_of_auxiliary(s)
    remove_dependents_of_fixed(s)
    remove_dependents_of_flat(s)
    remove_dependents_of_mark_case_cc(s)


def remove_dependents_of_auxiliary(s: Sentence) -> None:
    """
    Removes dependents from auxiliary verbs.

    In Universal Dependencies, auxiliary verbs typically cannot have dependents
    except for specific cases like negation. This function reattaches dependents
    of auxiliary verbs to their semantic governors.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        # Check if token is an auxiliary verb that shouldn't have dependents
        if t.upos == 'AUX' and not t.children_with_ud_label('conj') and not t.children_with_ud_label('cc') and t.children:

            # Find the semantic governor
            sgov = find_semantic_governor(t)

            if sgov and int(sgov.id) != 0:
                # Reattach dependents to the semantic governor
                for dep in t.children:
                    if dep.lemma != 'nie' and dep.dep_label != 'neg' and dep.udep_label != 'conj':
                        dep.ugov = sgov
                        logger.debug("Sentence %s: Reattached dependent %s from auxiliary %s to %s", t.sentence.id, dep.form, t.form, sgov.form)


def find_semantic_governor(t: Token) -> Optional[Token]:
    """
    Finds the semantic governor of a token.

    This function recursively traverses the dependency path upward,
    skipping auxiliary verbs, to find the semantic head of a token.

    :param Token t: The token to find the semantic governor for
    :return: The semantic governor token, or None if not found
    :rtype: Optional[Token]
    """
    # Start with the immediate governor
    gov = t.ugov

    # If no governor, return None
    if not gov:
        return None

    # If governor is an auxiliary verb, recursively find its governor
    if gov.upos == 'AUX':
        return find_semantic_governor(gov)

    # Otherwise, return the governor
    return gov


def remove_dependents_of_fixed(s: Sentence) -> None:
    """
    Removes dependents from fixed expressions.

    In Universal Dependencies, tokens that are part of fixed expressions
    cannot have dependents. This function reattaches dependents of fixed
    expression components to the head of the fixed expression.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.udep_label == 'fixed':
            # Find the head of the fixed expression
            fixed_head = t.super_gov_via_label('fixed')
            if fixed_head:
                fixed_head = fixed_head[0]

                # Find all tokens in the fixed expression
                fixed_tokens = collect_fixed_tokens(fixed_head)

                # Reattach dependents of fixed expression components to the head
                for fixed_token in fixed_tokens:
                    for dep in fixed_token.children:
                        if dep.ugov != fixed_head:
                            dep.ugov = fixed_head
                            logger.debug("Sentence %s: Reattached dependent %s from fixed token %s to %s", t.sentence.id, dep.form, fixed_token.form, fixed_head.form)
            else:
                logger.warning("Sentence %s: Fixed token %s has no super-governor.", t.sentence.id, t.form)
                continue


def collect_fixed_tokens(t: Token) -> List[Token]:
    """
    Collects all tokens that are part of a fixed expression.

    :param Token t: The head token of the fixed expression
    :return: List of tokens in the fixed expression
    :rtype: List[Token]
    """
    fixed_tokens = []

    # Find all direct dependents with 'fixed' relation
    direct_fixed = t.children_with_ud_label('fixed')
    fixed_tokens.extend(direct_fixed)

    # Recursively find dependents of fixed tokens
    for fixed in direct_fixed:
        fixed_tokens.extend(collect_fixed_tokens(fixed))

    return fixed_tokens


def remove_dependents_of_flat(s: Sentence) -> None:
    """
    Corrects flat structures to ensure left-to-right attachment.

    In Universal Dependencies, flat structures (like names) should be
    attached left-to-right. This function corrects cases where this
    constraint is violated.

    :param Sentence s: The sentence to process
    """
    # Iterate through all tokens in the sentence
    for t in s.tokens:
        # Find all flat dependents of the token
        flat_deps = t.children_with_ud_label('flat')

        for flat in flat_deps:
            # Check if flat dependent comes before its governor
            if int(flat.id) < int(t.id):
                if t.ugov:
                    flat.ugov = t.ugov
                    t.ugov = flat
                    logger.debug("Sentence %s: Reordered flat structure: %s -> %s", t.sentence.id, flat.form, t.form)
                else:
                    logger.warning("Sentence %s: Flat token %s has no UD governor.", t.sentence.id, t.form)


def remove_dependents_of_mark_case_cc(s: Sentence) -> None:
    """
    Removes dependents from mark, case, and cc nodes.

    In Universal Dependencies, function words like markers, case markers,
    and coordinating conjunctions typically cannot have dependents except
    for specific cases. This function reattaches their dependents to their
    governors.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.ugov and t.udep_label in ['mark', 'case', 'cc', 'cc:preconj']:
            # Iterate through all dependents of the token, UD and non-UD
            for c in list(set(t.children + t.uchildren)):
                # Check if the dependent should be reattached
                if (c.udep_label in ['punct', 'advmod', 'list', 'cop', 'obl', 'aux:clitic', 'advcl', 'mark', 'orphan'] and
                    c.dep_label != 'abbrev_punct'):
                    # Reattach the dependent to the governor
                    c.ugov = t.ugov
                    logger.debug("Sentence %s: Reattached dependent %s from %s %s to %s", t.sentence.id, c.form, t.udep_label, t.form, t.ugov.form)
