"""
Module for the conversion of copula constructions to Universal Dependencies format.

This module handles the conversion of predicative expressions with copula verbs
according to the Universal Dependencies guidelines. In UD, the copula is not treated
as the head of a clause, but rather the nonverbal predicate is the head.

The UD approach to copula constructions can be summarized as follows:
1. The copula relation (cop) is restricted to function words whose sole function is to link
    a nonverbal predicate to its subject and which do not add any meaning other than
    grammaticalized TAME categories.
2. The nonverbal predicate (adjective, noun, prepositional phrase, etc.) becomes the head
    of the clause, and the copula verb is attached to it with the 'cop' relation.
3. The subject is attached to the nonverbal predicate with an appropriate relation.
4. Other dependents of the copula are reattached to the nonverbal predicate.
"""
import logging
from utils.classes import Sentence, Token
from dependency.labels import convert_label as cl

logger = logging.getLogger('ud_converter.dependency.structures.copula')


def convert_copula(s: Sentence) -> None:
    """
    Converts copula constructions from MPDT format to UD format.

    This function identifies copula constructions and applies the appropriate
    conversion function based on the syntactic context.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        # Check for copula verbs with lemma 'to'
        if t.lemma == 'to' and t.pos == 'pred':
            # Check for different types of predicative expressions
            if t.children_with_label('subj'):
                if len(t.children_with_label('pd')) == 1:
                    if t.children_with_label('pd')[0].upos == 'ADJ':
                        convert_predicative_adj(t, t.gov)
                    else:
                        convert_predicative_other(t, t.gov, t.children_with_label('subj')[0])
                else:
                    logger.warning("Multiple predicative expressions found for copula: %s", t.form)
            else:
                convert_predicative_adj(t, t.gov)

        # Check for auxiliary verbs that function as copulas
        elif t.upos == 'AUX':
            # Example: "To było by zabawne, gdyby nie oferowali tej forsy."
            if t.children_with_label('pd') and t.gov:
                if len(t.children_with_label('pd')) == 1:
                    convert_predicative_adj(t, t.gov)
                else:
                    logger.warning("Multiple predicative expressions found for copula: %s", t.form)

        # Check for coordinated copula constructions
        elif t.upos == 'CCONJ' and len(t.children_with_label('conjunct')) > 1:
            if t.children_with_label('conjunct')[0].lemma in ['być', 'bywać']:
                if t.children_with_label('pd') and t.gov:
                    if len(t.children_with_label('pd')) == 1:
                        convert_coordinated_copula(t, t.gov)
                    else:
                        logger.warning("Multiple predicative expressions found for copula: %s", t.form)

        else:
            logger.warning('No conversion for copula structure: %s', t.form)


def convert_predicative_adj(cop: Token, gov: Token) -> None:
    """
    Converts a predicative expression with an adjectival predicate.

    In this construction, the adjectival predicate becomes the head of the clause,
    and the copula verb is attached to it with the 'cop' relation.

    Example: "To było piękne."

    :param Token cop: The copula token
    :param Token gov: The governor of the copula
    """
    # Find the predicative complement (pd)
    pds = cop.children_with_label('pd')

    if len(pds) == 1:
        pd = pds[0]
        subj = cop.children_with_label('subj')

        if subj:
            # Example: "Widok to niezapomniany"
            # Attach the subject to the predicative complement
            subj[0].ugov = pd
            subj[0].udep_label = cl(cop.dep_label)

        # Attach the predicative complement to the governor
        pd.ugov = gov
        pd.udep_label = cop.udep_label

        # Attach the copula to the predicative complement
        cop.ugov = pd
        cop.udep_label = 'cop'

        # Process other dependents of the copula
        process_copula_dependents(cop, pd, subj[0] if subj else None)
    elif len(pds) > 1:
        logger.warning("Multiple predicative expressions found for copula: %s", cop.form)


def convert_predicative_other(cop: Token, gov: Token, subj: Token) -> None:
    """
    Converts a predicative expression without an adjectival predicate.

    In this construction, the subject becomes the head of the clause,
    and the copula verb is attached to it with the 'cop' relation.

    Example: "To jest miłość"

    :param Token cop: The copula token
    :param Token gov: The governor of the copula
    :param Token subj: The subject token
    """
    pd = cop.children_with_label('pd')

    if pd:
        # Example: "Druga strefa to świat handlu eleganckiego"

        # Attach the subject to the governor
        subj.ugov = gov
        subj.udep_label = cop.udep_label

        # Attach the predicative complement to the subject
        pd[0].ugov = subj
        pd[0].udep_label = cl(pd[0].dep_label)

    else:
        # Example: "To jest miłość"

        # Attach the subject to the governor
        subj.ugov = gov
        subj.udep_label = '_'

    # Attach the copula to the subject
    cop.ugov = subj
    cop.udep_label = 'cop'

    # Process other dependents of the copula
    process_copula_dependents(cop, subj, pd[0] if pd else None)


def convert_coordinated_copula(cop: Token, gov: Token) -> None:
    """
    Converts a predicative expression with a coordinated copula.

    Examples: "Sztab Generalny jest i będzie czysty",
        "potęgą przemysłowo-gospodarczą owo państwo nie jest i nie było"
    
    :param Token cop: The copula token
    :param Token gov: The governor of the copula
    """
    pd = cop.children_with_label('pd')

    if pd:
        pd = pd[0]
        subj = cop.children_with_label('subj')

        if subj:
            # Attach the subject to the predicative complement
            subj[0].ugov = pd
            subj[0].udep_label = cl(subj[0].dep_label)

            # Attach the predicative complement to the governor
            pd.ugov = gov
            pd.udep_label = cop.udep_label

            # Attach the copula to the predicative complement
            cop.ugov = pd
            cop.udep_label = 'cop'

        for c in cop.children:
            if subj and c == subj[0]:
                continue
            if c != pd and c.dep_label not in ['neg', 'cneg', 'conjunct'] and c.lemma != 'nie':
                # Attach other dependents to the predicative complement
                c.ugov = pd
                c.udep_label = '_'


def process_copula_dependents(cop: Token, new_head: Token, exclude: Token = None) -> None:
    """
    Processes the dependents of a copula verb.

    In UD, dependents of a copula are attached to the nonverbal predicate.
    This function reattaches all dependents of the copula to the new head,
    except for the specified excluded token.

    :param Token cop: The copula token
    :param Token new_head: The new head token (nonverbal predicate)
    :param Token exclude: Optional token to exclude from reattachment
    """
    # Get all dependents of the copula
    dependents = cop.children

    # Create a list of tokens to exclude from reattachment
    exclude_list = []
    if exclude:
        exclude_list.append(exclude)

    # Add predicative complements and subjects to the exclude list
    exclude_list.extend(cop.children_with_label('pd'))
    exclude_list.extend(cop.children_with_label('subj'))

    # Reattach all other dependents to the new head
    for dep in dependents:
        if dep not in exclude_list and dep.dep_label not in ['neg', 'cneg']:
            # Attach the dependent to the new head
            dep.ugov = new_head
            # Keep the original dependency label
            dep.udep_label = dep.udep_label
