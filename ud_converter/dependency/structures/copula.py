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
from utils.classes import Sentence, Token
from utils.logger import ChangeCollector
from dependency.labels import convert_label as cl


def convert_copula(s: Sentence) -> None:
    """
    Converts copula constructions from MPDT format to UD format.

    This function identifies copula constructions and applies the appropriate
    conversion function based on the syntactic context.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        # Check for copula verbs with lemma 'to'
        if t.lemma == 'to' and t.pos == 'pred' and t.gov_id:
            # Check for different types of predicative expressions
            if t.children_with_label('subj'):
                if len(t.children_with_label('pd')) == 1 and t.children_with_label('pd')[0].upos == 'ADJ':
                    convert_predicative_adj(t, t.gov_id)
                else:
                    convert_predicative_other(t, t.gov_id, t.children_with_label('subj')[0])

            else:
                convert_predicative_adj(t, t.gov_id)

        # Check for auxiliary verbs that function as copulas
        elif t.upos == 'AUX':
            # Example: "To było by zabawne, gdyby nie oferowali tej forsy."
            if t.children_with_label('pd'):
                if len(t.children_with_label('pd')) == 1:
                    convert_predicative_adj(t, t.gov_id)
                else:
                    ChangeCollector.record(t.sentence.id, t.id, f"Multiple predicative expressions found for copula: '{t.form}'", module="structures.copula2", level='warning')

        # Check for coordinated copula constructions
        elif t.upos == 'CCONJ' and len(t.children_with_label('conjunct')) > 1:
            if t.children_with_label('conjunct')[0].lemma in ['być', 'bywać']:
                if t.children_with_label('pd') and t.gov:
                    if len(t.children_with_label('pd')) == 1:
                        convert_coordinated_copula(t, t.gov)
                    else:
                        ChangeCollector.record(t.sentence.id, t.id, f"Multiple predicative expressions found for copula: '{t.form}'", module="structures.copula3", level='warning')


def convert_predicative_adj(cop: Token, gov_id: str) -> None:
    """
    Converts a predicative expression with an adjectival predicate.

    In this construction, the adjectival predicate becomes the head of the clause,
    and the copula verb is attached to it with the 'cop' relation.

    Example: "To było piękne."

    :param Token cop: The copula token
    :param str gov_id: The governor_id of the copula
    """
    # Find the predicative complement (pd)
    pds = cop.children_with_label('pd')

    if len(pds) == 1:
        pd = pds[0]
        subj = cop.children_with_label('subj')

        if subj:
            # Example: "Widok to niezapomniany"
            # Attach the subject to the predicative complement
            ChangeCollector.record(cop.sentence.id, subj[0].id, f"Subject '{subj[0].form}' attached to predicative complement '{pd.form}'", module="structures.copula1")
            subj[0].udep_label = cl(subj[0])
            subj[0].ugov = pd
            subj[0].gov = pd
            subj[0].dep_label = 'subj'

        # Attach the predicative complement to the governor
        ChangeCollector.record(cop.sentence.id, pd.id, f"Predicative complement '{pd.form}' attached to governor '{gov_id}'", module="structures.copula2")
        pd.ugov_id = gov_id
        pd.gov_id = gov_id
        pd.udep_label = cop.udep_label
        pd.dep_label = cop.dep_label

        # Attach the copula to the predicative complement
        ChangeCollector.record(cop.sentence.id, cop.id, f"Copula '{cop.form}' attached to predicative complement '{pd.form}'", module="structures.copula3")
        cop.ugov = pd
        cop.gov = pd
        cop.udep_label = 'cop'

        # Process other dependents of the copula
        process_copula_dependents(cop, pd, subj[0] if subj else None)
    elif len(pds) > 1:
        ChangeCollector.record(cop.sentence.id, cop.id, f"Multiple predicative expressions found for copula: '{cop.form}'", module="structures.copula4", level='warning')


def convert_predicative_other(cop: Token, gov_id: str, subj: Token) -> None:
    """
    Converts a predicative expression without an adjectival predicate.

    In this construction, the subject becomes the head of the clause,
    and the copula verb is attached to it with the 'cop' relation.

    Example: "To jest miłość"

    :param Token cop: The copula token
    :param str gov_id: The governor ID of the copula
    :param Token subj: The subject token
    """
    pd = cop.children_with_label('pd')

    if pd:
        # Example: "Druga strefa to świat handlu eleganckiego"

        # Attach the predicative complement to the subject
        ChangeCollector.record(cop.sentence.id, pd[0].id, f"Predicative complement '{pd[0].form}' attached to subject '{subj.form}'", module="structures.copula5")
        pd[0].ugov = subj
        pd[0].gov = subj
        pd[0].udep_label = cl(subj, n=pd[0], gov=cop)
        pd[0].dep_label = 'subj'

        # Attach the subject to the governor
        ChangeCollector.record(cop.sentence.id, subj.id, f"Subject '{subj.form}' attached to governor '{gov_id}'", module="structures.copula4")
        subj.ugov_id = gov_id
        subj.gov_id = gov_id
        subj.udep_label = cop.udep_label
        subj.dep_label = cop.dep_label

    else:
        # Example: "To jest miłość"

        # Attach the subject to the governor
        ChangeCollector.record(cop.sentence.id, subj.id, f"Subject '{subj.form}' attached to governor '{gov_id}'", module="structures.copula6")
        subj.ugov_id = gov_id
        subj.gov_id = gov_id
        subj.udep_label = '_'
        subj.dep_label = cop.dep_label

    # Attach the copula to the subject
    ChangeCollector.record(cop.sentence.id, cop.id, f"Copula '{cop.form}' attached to subject '{subj.form}'", module="structures.copula7")
    cop.ugov = subj
    cop.gov = subj
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
        pd_t = pd[0]
        subj = cop.children_with_label('subj')

        if subj:
            # Attach the subject to the predicative complement
            ChangeCollector.record(cop.sentence.id, subj[0].id, f"Subject '{subj[0].form}' attached to predicative complement '{pd_t.form}'", module="structures.copula8")
            subj[0].udep_label = cl(subj[0])
            subj[0].dep_label = 'subj'
            subj[0].ugov = pd_t
            subj[0].gov = pd_t
            

            # Attach the predicative complement to the governor
            ChangeCollector.record(cop.sentence.id, pd_t.id, f"Predicative complement '{pd_t.form}' attached to governor '{gov.form}'", module="structures.copula9")
            pd_t.ugov = gov
            pd_t.gov = gov
            pd_t.udep_label = cop.udep_label
            pd_t.dep_label = cop.dep_label

            # Attach the copula to the predicative complement
            ChangeCollector.record(cop.sentence.id, cop.id, f"Copula '{cop.form}' attached to predicative complement '{pd_t.form}'", module="structures.copula10")
            cop.ugov = pd_t
            cop.gov = pd_t
            cop.udep_label = 'cop'

        for c in cop.children:
            if subj and c == subj[0]:
                continue
            if c != pd_t and c.dep_label not in ['neg', 'cneg', 'conjunct'] and c.lemma != 'nie':
                # Attach other dependents to the predicative complement
                ChangeCollector.record(cop.sentence.id, c.id, f"Dependent '{c.form}' attached to predicative complement '{pd_t.form}'", module="structures.copula11")
                c.ugov = pd_t
                c.gov = pd_t
                c.udep_label = '_'


def process_copula_dependents(cop: Token, new_head: Token, exclude: Token | None = None) -> None:
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
            ChangeCollector.record(cop.sentence.id, dep.id, f"Dependent '{dep.form}' attached to new head '{new_head.form}'", module="structures.copula12")
            dep.ugov = new_head
            dep.gov = new_head
