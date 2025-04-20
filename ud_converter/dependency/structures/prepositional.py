"""
Module for the conversion of prepositional phrases from MPDT to UD format, including prepositional phrases in coordination structures.

The conversion follows Universal Dependencies guidelines, making the complement
of the preposition the head of the prepositional phrase and attaching the
preposition to its complement with a 'case' relation.
"""
from utils.logger import ChangeCollector
from utils.classes import Sentence, Token


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
                if not t.super_gov_via_label('mwe'):
                    ChangeCollector.record(t.sentence.id, t.id, f"Super-governor not found for preposition: '{t.form}'", module="structures.prepositional", level='WARNING')
                    continue
                super_gov = t.super_gov_via_label('mwe')[0] # type: ignore
                super_gov_child = t.super_gov_via_label('mwe')[1] # type: ignore
                if super_gov and super_gov.udep_label == '_' and super_gov.dep_label in ['adjunct_compar', 'adjunct_comment']:
                    # Skip comparative and comment adjuncts
                    ChangeCollector.record(t.sentence.id, t.id, f"Skipping comparative or comment adjunct (preposition): '{t.form}'", module="structures.prepositional", level='WARNING')
                else:
                    # Convert the prepositional phrase
                    convert_pp(super_gov_child, super_gov, t)
                    ChangeCollector.record(t.sentence.id, t.id, f"Converted prepositional phrase: '{t.form}'", module="structures.prepositional")
            else:
                # Convert standard prepositional phrases
                convert_pp(t, t.gov, t)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted prepositional phrase: '{t.form}'", module="structures.prepositional")


def convert_pp(prep: Token, gov: Token, t: Token) -> None:
    """
    Helper function for converting a prepositional phrase to UD format.

    In UD, the complement of the preposition becomes the head of the phrase,
    and the preposition is attached to its complement with a 'case' relation.

    :param Token prep: The preposition token or child of the super-governor
    :param Token gov: The super-governor of the preposition
    :param Token t: The preposition token
    """
    # Find the complements of the preposition but only on the right side
    comp = [c for c in t.children_with_label('comp') if int(c.id) > int(prep.id)]

    if not comp:
        # Try to find a complement through a multiword expression
        mwe_comp = t.super_child_with_label_via_label('comp', 'mwe')

        if not mwe_comp:
            # Handle special cases like "obok lub zamiast jednostek"
            if prep.dep_label == 'conjunct' and gov.udep_label != 'case' and t.gov:
                conj_comp = t.gov.children_with_label('comp')

                if not conj_comp:
                    if prep.dep_label == 'comp' and gov and gov.upos in ['VERB', 'ADV']:
                        # Handle orphaned obliques
                        prep.udep_label = 'obl:orphan'
                    else:
                        ChangeCollector.record(t.sentence.id, t.id, f"The preposition '{prep.form}' has no complements", module="structures.prepositional", level='WARNING')
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
                        ChangeCollector.record(t.sentence.id, t.id, f"The preposition '{prep.form}' has {len(conj_comp)} complements: {[c.form for c in conj_comp]}", module="structures.prepositional", level='WARNING')
            else:
                ChangeCollector.record(t.sentence.id, t.id, f"The preposition '{prep.form}' has no complements", module="structures.prepositional", level='WARNING')
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
            ChangeCollector.record(t.sentence.id, t.id, f"The preposition '{prep.form}' has {len(comp)} complements: {[c.form for c in comp]}", module="structures.prepositional", level='WARNING')


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
