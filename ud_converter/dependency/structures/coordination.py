"""
Module for the conversion of coordination structures to Universal Dependencies format.

This module handles the conversion of various types of coordination structures:
- Standard coordination with conjunctions (e.g., 'Siedzi i czyta.')
- Coordination with punctuation marks (e.g., 'Siedzi, czyta.')
- Coordination with compound conjunctions (e.g., 'przy czym', 'przy tym')
- Pre-conjunctions (e.g., the first 'albo' in 'albo ... albo ...')
- Shared dependents across conjuncts

The conversion follows Universal Dependencies guidelines, making the first conjunct
the head of the coordination structure and attaching coordinating conjunctions to
the immediately succeeding conjunct.
"""
import re
from utils.logger import ChangeCollector
from utils.classes import Sentence, Token
from dependency.labels import convert_label as cl


# Regular expressions for identifying shared dependents
RE_SHARED = re.compile(r'^(subj|obj|adjunct|comp|cop|obl|cond|aux|vocative|app|pd|orphan|item|aglt|refl|imp|ne|cneg)')
RE_SHARED2 = re.compile(r'(cop|case|mark|det:numgov|nummod)')


def convert_coordination(s: Sentence) -> None:
    """
    Converts coordination structures from MPDT format to UD format.

    This function identifies different types of coordination structures and applies
    the appropriate conversion function based on the syntactic context.

    :param Sentence s: The sentence to convert
    """
    # Process tokens in post-order to handle nested structures correctly
    for t in s.tokens:
        # Coordination with a coordinating conjunction, e.g. "Siedzi i czyta."
        if t.upos == 'CCONJ' and t.children_with_label('conjunct') and t.gov:
            coordination(t, False)
            ChangeCollector.record(t.sentence.id, t.id, f"Converted coordination structure: '{t.form}'", module="structures.coordination")

        # Coordination with the compound conjunctions "przy czym", "przy tym"
        elif t.lemma == 'przy' and t.next and t.next.form in ['czym', 'tym'] and t.children_with_label('conjunct') and t.gov:
            # Mark the compound conjunction as fixed
            if t.next and t.next.gov == t and t.next.dep_label == 'mwe':
                t.next.udep_label = 'fixed'
            coordination(t, False)
            ChangeCollector.record(t.sentence.id, t.id, f"Converted coordination structure: '{t.form}'", module="structures.coordination")

        # Coordination with a punctuation mark used as a conjunction, e.g. "Siedzi, czyta."
        elif t.upos == 'PUNCT' and t.children_with_label('conjunct') and t.gov:
            conjuncts = t.children_with_label('conjunct')
            if t.udep_label != 'conj' and conjuncts and conjuncts[0].udep_label not in ['punct', 'cc']:
                coordination(t, True)
                ChangeCollector.record(t.sentence.id, t.id, f"Converted coordination structure: '{t.form}'", module="structures.coordination")
            else:
                # Treatment of cases with a conjunct realized as a coordination
                # e.g. "nie wziął udziału, ale teraz to wszystko odrobi, nadgoni"
                if t.udep_label == 'conj' and t.children_with_label('conjunct'):
                    coordination(t, True, ud_label='conj')
                    ChangeCollector.record(t.sentence.id, t.id, f"Converted coordination structure: '{t.form}'", module="structures.coordination")
                else:
                    ChangeCollector.record(t.sentence.id, t.id, f"No conversion for coordination structure: '{t.form}'", module="structures.coordination", level='WARNING')


def coordination(t: Token, punct_conj: bool, ud_label: str | None = None) -> None:
    """
    Converts a coordination structure to UD format.

    This function handles the core conversion of coordination structures, including
    the reattachment of conjuncts, shared dependents, and other elements.

    :param Token t: The conjunction token (CCONJ or PUNCT)
    :param bool punct_conj: Whether the coordination uses punctuation as a conjunction
    :param str ud_label: Optional specific UD label to use for the coordination
    """
    # Split the dependents of the conjunction token
    children = t.children
    # conjuncts (coordinated elements)
    conjuncts = [c for c in children if c.udep_label == '_' and c.dep_label == 'conjunct']
    # pre-conjunctions (e.g., the first 'albo' in 'albo ... albo ...')
    pre_coords = [c for c in children if c.udep_label == '_' and c.dep_label == 'pre_coord' and int(c.id) < int(t.id)]
    # Punctuation marks
    puncts = [c for c in children if c.dep_label == 'punct']
    # Shared dependents (arguments and modifiers shared by all conjuncts)
    shared = [c for c in children if (c not in conjuncts + pre_coords + puncts
              and c.udep_label != 'fixed'
              and (RE_SHARED.search(c.dep_label)
                   or RE_SHARED2.search(c.udep_label)
                   or (c.dep_label == 'mwe' and c.pos == 'brev')
                   or (c.dep_label == 'mwe' and c.pos == 'subst' and c.form != 'czym')))]
    # Other dependents
    other = [c for c in children if c not in conjuncts + pre_coords + puncts + shared]

    if not conjuncts or len(conjuncts) < 1:
        return

    # main_c is the first coordinated conjunct, which is the head in UD
    main_c = sorted(conjuncts, key=lambda x: int(x.id))[0]

    # Conversion of coordination structures with punctuation marks
    if punct_conj:
        # Attach the first conjunct to the governor
        if t.gov:
            main_c.ugov = t.gov
            main_c.udep_label = ud_label if ud_label else t.gov.udep_label

        # Handle enhanced dependencies
        if t.dep_label == 'conjunct':
            # Add enhanced dependency from the super-governor to the main conjunct
            if t.gov and t.gov.gov and len(t.gov.gov.children_with_label('conjunct')) == 0:
                main_c.eud = {t.gov.gov.id: cl(t.gov)}
        elif t.gov and t.gov.id not in main_c.eud and t.gov.pos != 'conj':
            main_c.eud = {t.gov.id: cl(t.gov)}

        puncts.append(t)

    # Conversion of coordination structures with conjunctions
    else:
        # Attach the first conjunct to the governor
        if t.gov:
            main_c.ugov = t.gov
            main_c.udep_label = ud_label if ud_label else t.udep_label
            t.udep_label = 'cc'

        # Find the next conjunct after the conjunction
        next_conjunct = find_next_token(conjuncts, t)
        if next_conjunct:
            # Attach the conjunction to the next conjunct (UD v2 guideline)
            t.ugov = next_conjunct
        else:
            # If no next conjunct, attach to the main conjunct
            t.ugov = main_c

            # Handle enhanced dependencies
            if t.gov and t.dep_label != 'conjunct' and cl(main_c) != '_' and t.gov.id not in main_c.eud:
                main_c.eud = {t.gov.id: cl(main_c)}

    # Process other elements of the coordination structure
    process_puncts(puncts, conjuncts)
    process_conjuncts(conjuncts, main_c, t)
    process_precoords(pre_coords, conjuncts)
    process_shared(shared, conjuncts, main_c)
    process_other(other, conjuncts, main_c, t)


def find_next_token(tokens: list[Token], t: Token) -> Token | None:
    """
    Finds the next token from the given list after the specified token.

    :param List[Token] tokens: List of tokens
    :param Token t: The token
    :return: The next token from the given list after the specified token, or None if not found
    :rtype: Token | None
    """
    # Sort tokens by ID
    sorted_tokens = sorted(tokens, key=lambda x: int(x.id))

    # Find the first token (in the list) that comes after the specified token
    for c in sorted_tokens:
        if int(c.id) > int(t.id):
            return c

    return None


def process_conjuncts(conjuncts: list[Token], main_c: Token, t: Token) -> None:
    """
    Processes the conjuncts in a coordination structure.

    :param List[Token] conjuncts: List of conjunct tokens
    :param Token main_c: The main (first) conjunct
    :param Token t: The conjunction token
    """
    # Skip the main conjunct
    for c in conjuncts:
        if c != main_c:
            # Attach other conjuncts to the main conjunct with 'conj' relation
            c.ugov = main_c
            c.udep_label = 'conj'
            if c.pos == 'conj' and [cc for cc in c.children_with_label('conjunct') if cc.udep_label == '_']:
                min_cc = min([cc for cc in c.children_with_label('conjunct') if cc.udep_label == '_'], key=lambda x: int(x.id))
                min_cc.eud = {main_c.id: 'conj'}
            else:
                c.eud = {main_c.id: 'conj'}
            if t.dep_label == 'conjunct' and t.udep_label == '_' and t.gov:
                temp_c = min([cc for cc in t.gov.children_with_label('conjunct') if cc.udep_label == '_'], key=lambda x: int(x.id))
                temp_successors = [cc for cc in temp_c.children_with_label('conjunct') if cc.udep_label == '_']
                if temp_successors:
                    temp2 = min(temp_successors, key=lambda x: int(x.id))
                    c.eud = {temp2.id: 'conj'}
                else:
                    c.eud = {temp_c.id: 'conj'}
            else:
                # shared argument, eg. "ministrowie i generałowie" - here is the conversion of the second conjunct, i.e. "generałowie"
                if t.gov and t.gov.id not in c.eud and t.gov.upos == 'CCONJ':
                    enhanced_conjuncts = []
                    for govc in t.gov.children_with_label('conjunct'):
                        if govc.udep_label == '_':
                            # if conjunct is a conjunction, then we have a coordination structure and we need to find the first conjunct of this coordination
                            if govc.pos == 'conj':
                                enhanced_conjuncts.append(min([cc for cc in govc.children_with_label('conjunct') if cc.udep_label == '_'], key=lambda x: int(x.id)))
                            else:
                                enhanced_conjuncts.append(govc)
                    if enhanced_conjuncts:
                        for ec in enhanced_conjuncts:
                            c.eud = {ec.id: cl(t)}
                else:
                    if c.pos == 'conj' and [cc for cc in c.children_with_label('conjunct') if cc.udep_label == '_']:
                        min_cc = min([cc for cc in c.children_with_label('conjunct') if cc.udep_label == '_'], key=lambda x: int(x.id))
                        c.eud = {min_cc.id: cl(t)}
                    elif t.gov:
                        c.eud = {t.gov.id: cl(t)}


def process_puncts(puncts: list[Token], conjuncts: list[Token]) -> None:
    """
    Processes punctuation marks in a coordination structure.

    :param List[Token] puncts: List of punctuation tokens
    :param List[Token] conjuncts: List of conjunct tokens
    """
    for p in puncts:
        # Find the nearest conjunct after the punctuation
        next_token = find_next_token(conjuncts, p)
        if next_token:
            p.ugov = next_token
        p.udep_label = 'punct'


def process_precoords(pre_coords: list[Token], conjuncts: list[Token]) -> None:
    """
    Processes pre-conjunctions in a coordination structure, e.g., the first "albo" in "albo ... albo ...".

    :param List[Token] pre_coords: List of pre-conjunction tokens
    :param List[Token] conjuncts: List of conjunct tokens
    """
    for pre in pre_coords:
        # Find conjuncts that come after the pre-conjunction
        later_conjuncts = [c for c in conjuncts if int(c.id) > int(pre.id)]

        if later_conjuncts:
            # Attach pre-conjunction to the nearest following conjunct
            pre.ugov = min(later_conjuncts, key=lambda x: int(x.id))
            pre.udep_label = 'cc:preconj'


def process_shared(shared: list[Token], conjuncts: list[Token], main_c: Token) -> None:
    """
    Processes shared dependents in a coordination structure.

    :param List[Token] shared: List of shared dependent tokens
    :param List[Token] conjuncts: List of conjunct tokens
    :param Token main_c: The main (first) conjunct
    """
    for s in shared:
        # Attach shared dependent to the main conjunct
        s.ugov = main_c
        s.udep_label = cl(s)

        # Enhanced dependencies for shared dependents
        for con in conjuncts:
            s.eud = {con.id: cl(s)}


def process_other(other: list[Token], conjuncts: list[Token], main_c: Token, t: Token) -> None:
    """
    Processes other dependents in a coordination structure.

    :param List[Token] other: List of other dependent tokens
    :param Token main_c: The main (first) conjunct
    :param Token t: The conjunction token
    """
    for o in other:
        if o.dep_label == 'mwe':
            # Multiword expressions are handled separately
            pass

        # Coordinating conjunction with a conjunct realized as a coordination
        # e.g. "zaś" in "Mulla zaś ... pozostawal niewidzalny, bez twarzy."
        elif o.upos == 'CCONJ' and o.udep_label == 'cc':
            o.ugov = main_c
            o.udep_label = 'cc'
            o.eud = {main_c.id: 'cc'}

        # Punctuation with special handling
        elif o.pos == 'interp' and t.pos == 'conj' and o.dep_label != 'punct' and not o.children:
            o.ugov = main_c
            o.udep_label = 'punct'

        # Subordinating conjunction with a dependent realized as a coordination
        # e.g. "bo" in "... tworząc jeziora ..., bo głęboka płyta ... uległa zgnieceniu, a wody zapełniły ..."
        elif o.upos == 'SCONJ' and o.udep_label == 'mark':
            o.ugov = main_c
            o.udep_label = 'mark'
            for con in conjuncts:
                o.eud = {con.id: 'mark'}

        # Default case
        else:
            o.ugov = main_c
            o.udep_label = 'mark'
