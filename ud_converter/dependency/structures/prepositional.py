"""
Module for the conversion of prepositional phrases from MPDT to UD format, including prepositional phrases in coordination structures.

The conversion follows Universal Dependencies guidelines, making the complement
of the preposition the head of the prepositional phrase and attaching the
preposition to its complement with a 'case' relation.
"""
import logging
from utils.classes import Sentence, Token
from dependency.labels import convert_label as cl

logger = logging.getLogger('ud_converter.dependency.structures.prepositional')


def convert_prepositional(s: Sentence) -> None:
    """
    Converts prepositional phrases from MPDT to UD format.

    This function identifies prepositional phrases and applies the appropriate
    conversion function based on the syntactic context.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        if t.upos == 'ADP' and t.gov:
            if t.dep_label == 'mwe':
                # Handle prepositions that are part of multiword expressions
                super_gov = t.rec_gov_via_label('mwe')[0]
                super_gov_child = t.rec_gov_via_label('mwe')[1]
                if super_gov and super_gov.udep_label == '_' and super_gov.dep_label in ['adjunct_compar', 'adjunct_comment']:
                    # Skip comparative and comment adjuncts
                    logger.warning('Skipping comparative or comment adjunct (preposition): %s', t.form)
                else:
                    # Convert the prepositional phrase
                    convert_pp(super_gov_child, super_gov, t)
            else:
                # Convert standard prepositional phrases
                convert_pp(t, t.gov, t)


def convert_pp(prep: Token, gov: Token, t: Token) -> None:
    """
    Helper function for converting a prepositional phrase to UD format.

    In UD, the complement of the preposition becomes the head of the phrase,
    and the preposition is attached to its complement with a 'case' relation.

    :param Token prep: The preposition token or child of the super-governor
    :param Token gov: The super-governor of the preposition
    :param Token t: The prepostion token
    """
    # Find the complements of the preposition but only on the right side
    comp = [c for c in t.children_with_label('comp') if c.id > prep.id]

    if not comp:
        # Try to find a complement through a multiword expression
        mwe_comp = t.rec_child_with_label_via_label('comp', 'mwe')

        if not mwe_comp:
            # Handle special cases like "obok lub zamiast jednostek"
            if prep.dep_label == 'conjunct' and gov.udep_label != 'case':
                conj_comp = t.gov.children_with_label('comp')

                if not conj_comp:
                    if prep.dep_label == 'comp' and gov.upos in ['VERB', 'ADV']:
                        # Handle orphaned obliques
                        prep.udep_label = 'obl:orphan'
                    else:
                        logger.warning("The preposition '%s' has no complements", prep.form)
                else:
                    if len(conj_comp) == 1:
                        # Attach the complement to the super-governor
                        super_gov = gov.gov
                        if super_gov:
                            conj_comp[0].ugov = super_gov
                            conj_comp[0].udep_label = gov.udep_label

                            # Attach the conjunction to the complement
                            gov.ugov = conj_comp[0]
                            gov.udep_label = '_'
                    else:
                        logger.warning("The preposition '%s' has %d complements: %s",
                                      prep.form, len(conj_comp), [c.form for c in conj_comp])
            else:
                logger.warning("The preposition '%s' has no complements", prep.form)
        else:
            # Skip special case for "podczas gdy"
            if prep.lemma == 'podczas' and prep.next and prep.next.lemma == 'gdy':
                pass
            else:
                # Attach the MWE complement to the governor
                mwe_comp.ugov = gov
                mwe_comp.udep_label = prep.udep_label

                # Attach the preposition to the complement
                prep.ugov = mwe_comp
                prep.udep_label = 'case'

                # Process other dependents of the preposition
                convert_prep_dependents(prep, mwe_comp)
    else:
        if len(comp) == 1:
            # Standard case: one complement
            # Attach the complement to the governor
            comp[0].ugov = gov
            comp[0].udep_label = prep.udep_label

            # Attach the preposition to the complement
            prep.ugov = comp[0]
            prep.udep_label = 'case'

            # Process other dependents of the preposition
            convert_prep_dependents(prep, comp[0])
        else:
            logger.warning("The preposition '%s' has %d complements: %s",
                          prep.form, len(comp), [c.form for c in comp])


def convert_prep_dependents(t: Token, comp: Token) -> None:
    """
    Converts the dependents of a preposition.

    In UD, dependents of a preposition are attached to its complement.

    :param Token t: The preposition token
    :param Token comp: The complement of the preposition
    """
    # Get all dependents of the preposition except the complement
    dependents = [d for d in t.children if d != comp and d.dep_label not in ['mwe', 'abbrev_punct']]

    # Attach each dependent to the complement
    for d in dependents:
        d.ugov = comp
        d.udep_label = d.udep_label
