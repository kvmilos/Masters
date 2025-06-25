"""
Module for handling enhanced Universal Dependencies.

This module provides functions for completing enhanced dependency graphs
according to Universal Dependencies guidelines.
"""
from utils.logger import ChangeCollector
from utils.classes import Sentence, Token


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
    conj_eud_correction(s)
    add_extpos(s)


def add_extpos(s: Sentence) -> None:
    """
    Adds external part-of-speech tags to the adequate tokens in a sentence.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.upos == 'ADP' and t.udep_label.startswith('advmod'):
            t.data['ext_pos'] = 'ADV'


def complete_eud(s: Sentence) -> None:
    """
    Completes the enhanced dependency graph for a sentence.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if '-' not in t.id:
            if t.ugov_id == '_':
                # If the enhanced governor ID is '_', set it to the basic governor ID
                t.ugov_id = t.gov_id
                ChangeCollector.record(t.sentence.id, t.id, f"Setting gov -> ugov ({t.gov_id}) for token: '{t.form}'", module="postconversion")

            # Handle special cases for mark_rel
            if t.udep_label == 'mark_rel':
                ChangeCollector.record(t.sentence.id, t.id, f"Converting mark_rel to mark for token: '{t.form}'", module="postconversion")
                t.udep_label = 'mark'
                if t.ugov and t.ugov.gov_id != '0':
                    t.eud = {t.ugov.gov_id: 'ref'}

            # Add the basic dependency to the enhanced dependencies
            t.eud = {t.ugov_id: t.udep_label}

        # Update any placeholder governors in the enhanced-deps map
        for gov in list(t.data['eud'].keys()):
            label = t.data['eud'][gov]
            if gov.startswith('gov_'):
                # Log the replacement
                ChangeCollector.record(
                    t.sentence.id,
                    t.id,
                    f"Converting placeholder governor '{gov}' for token: '{t.form}'",
                    module="postconversion"
                )
                # Figure out the real ID to use
                tok = s.dict_by_id.get(gov.split('_', 1)[1])
                if tok:
                    real_id = tok.gov2_id  # this is either tok.ugov_id or tok.gov_id
                else:
                    # fallback: strip the "gov_" prefix
                    real_id = gov.split('_', 1)[1]

                # remove the placeholder and insert under the real ID
                del t.data['eud'][gov]
                if real_id != '0':
                    t.eud = {real_id: label}
            elif t.data['eud'][gov] == 'mark_rel':
                t.data['eud'][gov] = 'mark'

        # Convert any “_” labels to the true UD label without clobbering other entries
        for gov, lab in list(t.data['eud'].items()):
            if lab == '_' and t.ugov:
                ChangeCollector.record(
                    t.sentence.id,
                    t.id,
                    f"Converting placeholder label '_' to '{t.ugov.udep_label}' for token: '{t.form}'",
                    module="postconversion"
                )
                t.data['eud'][gov] = t.ugov.udep_label


def conj_eud_correction(s: Sentence) -> None:
    """
    Converts conjunct dependencies to enhanced dependencies.

    This function processes each token in the sentence and converts
    conjunct dependencies to enhanced dependencies according to the
    Universal Dependencies guidelines.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.udep_label == 'conj':
            # Reset enhanced dependencies to those of the governor, then add 'conj'
            deps = t.data['eud']
            deps.clear()
            for gov_key, gov_label in t.gov2.data['eud'].items():  # type: ignore
                if gov_label != 'root':
                    t.eud = {gov_key: gov_label}
            t.eud = {t.gov2_id: 'conj'}  # set the conjunct label


def default_label_conversion(s: Sentence) -> None:
    """
    Applies default label conversions for any remaining unconverted labels.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if t.udep_label == '_' and '-' not in t.id:
            if t.dep_label == 'conjunct':
                t.udep_label = 'case' if t.upos == 'ADP' else 'conj'
                ChangeCollector.record(t.sentence.id, t.id, f"Converting conjunct label to '{t.udep_label}' for token: '{t.form}'", module="postconversion")
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
        if 'PronType' in t.ufeats and t.ufeats['PronType'] == 'Int,Rel':
            visited: set = set()
            pronoun_type = look_for_clause_type(t, visited)
            if pronoun_type == 'Rel':
                t.ufeats['PronType'] = 'Rel'
            elif pronoun_type == 'Int':
                t.ufeats['PronType'] = 'Int'
            elif pronoun_type == 'Mwe':
                t.ufeats.pop('PronType', None)


def look_for_clause_type(t: Token | None, visited: set) -> str:
    """
    Determines the clause type for a pronoun based on its syntactic context.

    This function recursively examines the dependency path to determine
    whether a pronoun is used in a relative clause, an interrogative clause,
    a multiword expression, or as a root.

    :param Token t: The pronoun token
    :return: The clause type ('Rel', 'Int', 'Mwe', or '')
    :rtype: str
    """

    if isinstance(t, Token):
        # If we've already visited this token, we have a cycle
        if t.id in visited:
            ChangeCollector.record(t.sentence.id, t.id, f"Cycle detected in pronoun resolution for token '{t.form}'", module="postconversion", level='WARNING')
            return ''

        visited.add(t.id)

        if t.gov2_id:
            if t.udep_label == 'acl:relcl':
                return 'Rel'
            elif t.udep_label.startswith('ccomp') or t.udep_label.startswith('xcomp') or t.udep_label.startswith('advcl') or t.udep_label == 'root':
                return 'Int'
            elif t.udep_label == 'fixed':
                return 'Mwe'
            else:
                # print(t.to_string(form='mpdt'), t.to_string(form='ud'))
                return look_for_clause_type(t.gov2, visited)
        else:
            ChangeCollector.record(t.sentence.id, t.id, f"No governor found for pronoun: '{t.form}'", module="postconversion", level='WARNING')
            return ''
    return ''
