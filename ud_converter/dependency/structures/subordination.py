"""
Module for the conversion of subordinate clauses to Universal Dependencies format.

This module handles the conversion of various types of subordinate clauses:
- Simple subordinate clauses with conjunctions (e.g., 'że', 'żeby', 'ponieważ')
- Complex subordinate clauses with compound conjunctions (e.g., 'jako że', 'podczas gdy')
- Attributive constructions with 'jako'
- Special cases with multiword expressions (e.g., 'w miarę jak', 'w przypadku gdy')

The conversion follows Universal Dependencies guidelines, making the predicate
of the subordinate clause the head and attaching the subordinating conjunction
to it with a 'mark' relation.
"""
import logging
from typing import Optional
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.dependency.structures.subordination')


def convert_subordination(s: Sentence) -> None:
    """
    Converts subordinate clauses from MPDT format to UD format.
    
    This function identifies different types of subordinate clauses and applies
    the appropriate conversion function based on the syntactic context.
    
    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        # Simple subordinating conjunctions
        if t.upos == 'SCONJ' and t.gov:
            # Handle 'jako' constructions
            if t.lemma == 'jako' and not t.children_with_label('mwe'):
                jako(t)

            # Handle complex subordinating conjunctions like 'jako że', 'podczas gdy', etc.
            elif t.dep_label == 'mwe' and (
                (t.lemma == 'że' and t.gov.lemma == 'jako') or
                (t.lemma == 'gdyby' and t.gov.lemma == 'jak') or
                (t.lemma == 'gdy' and t.gov.lemma == 'podczas') or
                (t.lemma in ['że', 'iż'] and t.gov.lemma in ['pomimo', 'mimo']) or
                (t.lemma == 'więc' and t.gov.lemma == 'tak')
            ):
                if t.gov.gov:
                    complex_subordinating_conjunction(t)

            # Handle special multiword expressions like 'w miarę jak', 'w przypadku gdy', etc.
            elif t.dep_label == 'mwe' and (
                (t.lemma == 'jak' and t.gov.lemma == 'miara') or
                (t.lemma in ['gdy', 'gdyby', 'kiedy', 'jak'] and t.gov.lemma in ['przypadek', 'wypadek'])
            ):
                complex_subordinating_threeword_conjunction(t)

            # Handle standard subordinating conjunctions
            elif t.dep_label != 'mwe' and not t.children_with_label('mwe') and t.udep_label == '_':
                subordinating_conjunction(t)

        # Handle 'o ile' construction
        elif t.lemma == 'o' and any(c.lemma == 'ile' and c.dep_label == 'mwe' for c in t.children):
            ile_token = next(c for c in t.children if c.lemma == 'ile' and c.dep_label == 'mwe')
            complex_subordinating_conjunction(ile_token)


def jako(t: Token) -> None:
    """
    Converts attributive constructions with 'jako'.
    
    In UD, the predicate of the attributive clause becomes the head,
    and 'jako' is attached to it with a 'mark' relation.
    
    Example: "Widok jako niezapomniany" → nsubj(niezapomniany, Widok), mark(niezapomniany, jako)
    
    :param Token t: The 'jako' token
    """
    # Find the predicative complement (pd)
    pds = t.children_with_label('pd')

    if not pds:
        logger.warning("The attributive construction JAKO has no dependents.")
        return

    if len(pds) == 1:
        pd = pds[0]
        gov = t.gov

        # Attach the predicative complement to the governor
        if gov:
            pd.ugov = gov
            pd.udep_label = t.udep_label
        else:
            logger.warning("The attributive construction JAKO has no governor.")

        # Attach 'jako' to the predicative complement
        t.ugov = pd
        t.udep_label = 'mark'
    else:
        logger.warning("The attributive construction JAKO has %d dependents pd: %s",
                      len(pds), [p.form for p in pds])


def complex_subordinating_conjunction(t: Token) -> None:
    """
    Converts subordinate clauses with complex subordinating conjunctions.
    
    Examples: 'jako że', 'podczas gdy', 'mimo że', 'tak więc', 'o ile'
    
    In UD, the predicate of the subordinate clause becomes the head,
    and the subordinating conjunction is attached to it with a 'mark' relation.
    
    :param Token t: The second part of the complex conjunction
    """
    if not t.super_gov_via_label('mwe') and t.gov:
        logger.warning("Complex subordinating conjunction has no super-governor: %s %s",
                      t.gov.form, t.form)
        return

    super_gov = t.super_gov_via_label('mwe')[0] # type: ignore
    super_gov_child = t.super_gov_via_label('mwe')[1] # type: ignore

    if not super_gov and t.gov:
        logger.warning("Complex subordinating conjunction has no governor: %s %s",
                      t.gov.form, t.form)
        return

    # Find the complement of the subordinate clause
    comp = find_complement(t)

    if not comp:
        if t.lemma not in ['to']:
            logger.warning("Subordinate conjunction '%s' has no dependents.", t.lemma)
            return
        else:
            logger.debug("Subordinate conjunction '%s' which is a 'to' has no dependents.", t.lemma)
            return

    # Attach the complement to the super-governor
    comp.ugov = super_gov
    comp.udep_label = super_gov_child.udep_label

    # Attach the first part of the conjunction to the complement
    super_gov_child.ugov = comp
    super_gov_child.udep_label = 'mark'

    # Process punctuation marks
    punctuation_marks(t, comp)


def complex_subordinating_threeword_conjunction(t: Token) -> None:
    """
    Converts subordinate clauses with special multiword expressions.
    
    Examples: 'w miarę jak', 'w przypadku gdy', 'w wypadku gdyby'
    
    :param Token t: The last part of the complex conjunction
    """
    if not t.super_gov_via_label('mwe') and t.gov:
        logger.warning("Complex subordinating conjunction has no super-governor: %s %s",
                      t.gov.form, t.form)
        return

    super_gov = t.super_gov_via_label('mwe')[0] # type: ignore
    super_gov_child = t.super_gov_via_label('mwe')[1] # type: ignore

    if (not super_gov) and t.gov:
        logger.warning("Complex subordinating conjunction has no governor: %s %s",
                      t.gov.form, t.form)
        return

    # Find the complement of the subordinate clause
    comp = t.children_with_label('comp_fin')

    if not comp:
        logger.warning("Subordinate conjunction '%s' has no dependents.", t.lemma)
        return

    if len(comp) > 1:
        logger.warning("Subordinate conjunction '%s' has %d dependents comp_fin: %s",
                      t.lemma, len(comp), [c.form for c in comp])
        return

    comp = comp[0]

    # Attach the complement to the super-governor
    comp.ugov = super_gov
    comp.udep_label = super_gov_child.udep_label

    # Attach the first part of the conjunction to the complement
    super_gov_child.ugov = comp
    super_gov_child.udep_label = 'mark'

    # Process punctuation marks
    for punct in [c for c in super_gov_child.children if c.upos == 'PUNCT']:
        punct.ugov = comp
        punct.udep_label = 'punct'


def subordinating_conjunction(t: Token) -> None:
    """
    Converts subordinate clauses with simple subordinating conjunctions.
    
    Examples: 'że', 'żeby', 'ponieważ'
    
    In UD, the predicate of the subordinate clause becomes the head,
    and the subordinating conjunction is attached to it with a 'mark' relation.
    
    :param Token t: The subordinating conjunction token
    """

    if not t.gov:
        logger.warning("Subordinating conjunction has no governor: %s", t.form)
        return

    # Find the complement of the subordinate clause
    comp = find_complement(t)

    if not comp:
        if t.lemma not in ['to', 'dopóty'] and t.dep_label != 'dep':
            logger.warning("Subordinate conjunction '%s' has no dependents.", t.lemma)
        return

    # Attach the complement to the governor
    comp.ugov = t.gov
    comp.udep_label = t.udep_label

    # Attach the conjunction to the complement
    t.ugov = comp
    t.udep_label = 'mark'

    # Process punctuation marks
    punctuation_marks(t, comp)


def find_complement(t: Token) -> Optional[Token]:
    """
    Finds the complement of a subordinate clause.
    
    This function looks for complements in the following order:
    1. comp_fin (finite complement)
    2. comp_inf (infinitive complement)
    3. comp (other complement)
    
    :param Token t: The subordinating conjunction token
    :return: The complement token, or None if not found
    :rtype: Optional[Token]
    """
    # Try to find a finite complement
    comp_fin = t.children_with_label('comp_fin')
    if comp_fin:
        if len(comp_fin) == 1:
            return comp_fin[0]
        else:
            logger.warning("Subordinate conjunction '%s' has %d dependents comp_fin: %s",
                          t.lemma, len(comp_fin), [c.form for c in comp_fin])
            return None

    # Try to find an infinitive complement
    comp_inf = t.children_with_label('comp_inf')
    if comp_inf:
        if len(comp_inf) == 1:
            return comp_inf[0]
        else:
            logger.warning("Subordinate conjunction '%s' has %d dependents comp_inf: %s",
                          t.lemma, len(comp_inf), [c.form for c in comp_inf])
            return None

    # Try to find any other complement
    comp = t.children_with_label('comp')
    if comp:
        if len(comp) == 1:
            return comp[0]
        else:
            logger.warning("Subordinate conjunction '%s' has %d dependents comp: %s",
                          t.lemma, len(comp), [c.form for c in comp])
            return None

    return None


def punctuation_marks(t: Token, comp: Token) -> None:
    """
    Converts punctuation marks in a subordinate clause.
    
    In UD, punctuation marks cannot be dependents of 'mark', so they are
    attached to the predicate of the subordinate clause.
    
    :param Token t: The subordinating conjunction token
    :param Token comp: The complement token
    """
    for punct in [c for c in t.children if c.upos == 'PUNCT']:
        if not punct.children:
            punct.ugov = comp
            punct.udep_label = 'punct'
        else:
            logger.warning("Punctuation mark '%s' has dependents.", punct.form)
