"""
Module for the conversion of elliptical structures to Universal Dependencies format

This module handles the conversion of structures with elided predicates, where a
punctuation mark (typically a comma) serves as a placeholder for the missing
predicate. In UD, ellipsis is handled by promoting one of the dependents to
become the head of the elliptical clause, and attaching other dependents to it
with the 'orphan' relation to indicate a non-standard attachment.

The UD approach to ellipsis can be summarized as follows:
1. If the elided element has no overt dependents, we do nothing.
2. If the elided element has overt dependents, we promote one of these to take the role of the head.
3. If the elided element is a predicate and the promoted element is one of its arguments or adjuncts,
we use the 'orphan' relation when attaching other non-functional dependents to the promoted head.

Dependents are considered for promotion in the following order:
nsubj > obj > iobj > obl > advmod > csubj > xcomp > ccomp > advcl > dislocated > vocative
"""
import logging
from utils.classes import Sentence, Token

logger = logging.getLogger('ud_converter.dependency.structures.ellipsis')


def convert_ellipsis(s: Sentence) -> None:
    """
    Converts elliptical structures from MPDT format to UD format.

    This function identifies structures with elided predicates (where a punctuation mark
    serves as a placeholder for the missing predicate) and applies the appropriate
    conversion function based on the syntactic context.

    Following the UD guidelines, we promote one dependent to become the head of the
    elliptical clause, with preference given to subjects, then objects, then other dependents.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        if t.upos == 'PUNCT' and t.gov:
            # Check if this punctuation mark is a potential ellipsis marker
            if (t.dep_label not in ['punct', 'abbrev_punct', 'item'] and
                not t.children_with_label('conjunct')):

                # Try to find a suitable head for the elliptical structure
                subj = t.children_with_label('subj')
                if len(subj) == 1:
                    process_ellipsis(t, subj[0])
                    continue
                elif len(subj) > 1:
                    logger.warning("Multiple subjects found for elliptical structure at token: %s", t.form)

                obj = t.children_with_re_label('obj')
                if len(obj) == 1:
                    process_ellipsis(t, obj[0])
                    continue
                elif len(obj) > 1:
                    logger.warning("Multiple objects found for elliptical structure at token: %s", t.form)

                comp = t.children_with_re_label('comp')
                if len(comp) == 1:
                    process_ellipsis(t, comp[0])
                    continue
                elif len(comp) > 1:
                    logger.warning("Multiple complements found for elliptical structure at token: %s", t.form)

                adjunct = t.children_with_re_label('adjunct')
                if len(adjunct) == 1:
                    process_ellipsis(t, adjunct[0])
                    continue
                elif len(adjunct) > 1:
                    logger.warning("Multiple adjuncts found for elliptical structure at token: %s", t.form)

                # If no suitable head is found, log a warning
                if t.children:
                    logger.warning("No suitable head found for elliptical structure at token: %s", t.form)


def process_ellipsis(punct: Token, head: Token) -> None:
    """
    Processes an elliptical structure by promoting a dependent to be the head.

    In UD, elliptical structures are handled by promoting one of the dependents
    to be the head of the elliptical clause, and attaching other dependents to
    it with the 'orphan' relation. This is used when simple promotion would result
    in an unnatural and misleading dependency relation.

    For example, in "Mary won gold and Peter bronze", the subject "Peter" is promoted
    to the head position in the second conjunct. Attaching "bronze" to "Peter" with
    a standard relation would be misleading because "bronze" is not the object of "Peter".
    Therefore, the 'orphan' relation is used to indicate a non-standard attachment.

    :param Token punct: The punctuation token marking the ellipsis
    :param Token head: The token to promote as the head of the elliptical structure
    """
    # Get all dependents of the punctuation mark except the new head
    dependents = [d for d in punct.children if d != head]

    # Attach the new head to the governor of the punctuation mark
    if punct.gov:
        head.ugov = punct.gov
        head.udep_label = punct.udep_label

    # Attach the punctuation mark to the new head
    punct.ugov = head
    punct.udep_label = 'punct'

    # Process other dependents
    for d in dependents:
        # Punctuation marks keep their label
        if d.upos == 'PUNCT':
            d.ugov = head
            # Keep the original dependency label
        else:
            # Other dependents become orphans
            d.ugov = head
            d.udep_label = 'orphan'
