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
    unit_fixes(s)
    fix_fixed(s)
    add_extpos(s)
    complete_eud(s)
    eud_correction(s)


def fix_fixed(s: Sentence) -> None:
    """
    Fixes some 'fixed' dependency labels in a sentence.
    """
    for t in s.tokens:
        if t.children_with_ud_label('fixed'):
            if t.pos.startswith('brev'):
                for child in t.children_with_ud_label('fixed'):
                    child.udep_label = 'flat'
            elif t.lemma == 'po' and t.children_with_ud_label('fixed')[0].upos == 'NOUN':
                child = t.children_with_ud_label('fixed')[0]
                if t.gov2 and t.gov2.upos == 'NOUN':
                    child.ugov_id = t.gov2.gov2_id
                    child.udep_label = 'obl'
                    t.ugov_id = child.id
            elif t.upos == 'X' and t.children_with_ud_label('fixed')[0].upos == 'NOUN' and t.ugov:
                ugov_id = t.ugov_id
                child = t.children_with_ud_label('fixed')[0]
                t.ugov_id = t.children_with_ud_label('fixed')[0].id
                t.udep_label = 'nummod'
                child.udep_label = 'nmod'
                child.ugov_id = ugov_id
            elif t.lemma == 'ni' and all(t.children_with_ud_label('fixed')[i].lemma in ['w', 'co'] for i in range(len(t.children_with_ud_label('fixed')))):
                c1 = t.children_with_ud_label('fixed')[0] if t.children_with_ud_label('fixed')[0].lemma == 'w' else t.children_with_ud_label('fixed')[1]
                c2 = t.children_with_ud_label('fixed')[1] if t.children_with_ud_label('fixed')[0].lemma == 'w' else t.children_with_ud_label('fixed')[0]
                if t.gov2 and t.gov2.gov2:
                    c1.ugov = c2
                    c1.udep_label = 'case'
                    c2.ugov = t.gov2
                    c2.udep_label = 'obl:arg'
                    t.ugov = t.gov2.gov2
                    t.udep_label = 'advmod:neg'
            elif t.lemma == 'na' and t.children_with_ud_label('fixed')[0].upos == 'NOUN':
                child = t.children_with_ud_label('fixed')[0]
                if t.gov2 and t.udep_label == 'case':
                    child.ugov = t.gov2
                    child.udep_label = 'nmod'
                    t.ugov = child
            elif t.lemma == 'jeżeli' and t.children_with_ud_label('fixed')[0].upos == 'AUX' and t.children_with_ud_label('ccomp'):
                if t.gov2 and t.gov2.gov2:
                    newgov = t.gov2.gov2.children_with_ud_label('xcomp')[0]
                    t.ugov = t.gov2.gov2
                    t.udep_label = 'mark'
                    ccomp = t.children_with_ud_label('ccomp')[0]
                    ccomp.ugov = newgov
                    ccomp.udep_label = 'advcl'
            elif t.lemma == 'w' and t.children_with_ud_label('fixed')[0].upos == 'NOUN' and t.ufeats['Case'] == 'Loc' and t.gov2 and t.gov2.gov2:
                child = t.children_with_ud_label('fixed')[0]
                gov = t.gov2
                newgov = gov.gov2.children_with_ud_label('amod')[0]
                t.ugov = child
                gov.ugov = child
                child.ugov = newgov
                child.udep_label = 'obl'



def add_extpos(s: Sentence) -> None:
    """
    Adds external part-of-speech tags to the adequate tokens in a sentence,
    and for each token with a 'fixed' child, writes a 3-line report entry
    into extpos_report.txt.

    Report format per fixed-child:
      Sentence <sent_id> Tokens <parent_id>, <fixed_child_id>
      <sentence text>
      <parent.form> <parent.upos>, <child.form> <child.upos>, <parent.ufeats['ExtPos']>

    :param Sentence s: The sentence to process
    """
    report_path = "extpos_report.txt"
    # open once per sentence, append mode
    with open(report_path, "a", encoding="utf-8") as out:
        for t in s.tokens:
            fixed_children = t.children_with_ud_label('fixed')
            if not fixed_children:
                continue

            # set the ExtPos feature as before
            t.ufeats = {'ExtPos': extpos(t, t.children_with_ud_label('fixed'))}

            # for each fixed child, write a 3-line record + blank line
            for child in fixed_children:
                # 1) Sentence header
                out.write(f"Sentence {s.id} Tokens {t.id}, {child.id}\n")
                # 2) Original sentence text
                out.write(f"{s.text}\n")
                # 3) token forms, upos, and ExtPos
                ext = t.ufeats.get('ExtPos', '')
                out.write(f"{t.form} {t.upos}, {child.form} {child.upos}, {ext}\n")
                # blank line between entries
                out.write("\n")


def extpos(t: Token, ch: list[Token]) -> str:
    """
    Determines the external part-of-speech tag for a token and child(ren).

    :param Token token: The token to analyze
    :param list[Token] fixed_children: The fixed children of the token
    :return: The external part-of-speech tag
    :rtype: str
    """
    if len(ch) > 1:
        print(f'LOL {t.sentence.id} {t.form} {[c.form for c in ch]}')
    c = ch[0]
    if t.upos == 'ADP' and t.udep_label.startswith('advmod'):
        return 'ADV'
    elif c.lemma == 'i':
        if t.lemma == 'jako':
            t.upos = 'SCONJ'
            return 'SCONJ'
        return 'CCONJ'
    elif t.upos == 'DET' and t.ufeats['Case'] == 'Ins' and c.upos == 'NOUN':
        return 'ADV'
    elif t.upos == 'PART' and c.upos == 'ADV':
        return 'ADV'
    elif t.lemma == 'to' and t.upos == 'PART' and c.lemma == 'być' and c.upos == 'VERB' and t.udep_label == 'advmod:emph':
        return 'CCONJ'
    return t.upos


def unit_fixes(s: Sentence) -> None:
    """
    Fixes certain issues in the dependency graph for a sentence.
    """
    for t in s.tokens:
        if t.lemma == 'jako' and t.children_with_lemma('ż') and t.dep_label == 'adjunct_caus':
            ze = t.children_with_lemma('ż')[0]
            ze.udep_label = 'fixed'
            shead = t.children_with_ud_label('ccomp')[0]
            gov = t.ugov
            shead.ugov = gov  # type: ignore
            shead.udep_label = 'advcl'
            t.ugov = shead
            t.udep_label = 'mark'
            t.eud.clear()
        elif t.lemma == 'jako' and t.children_with_ud_label('xcomp:pred') and t.gov.upos == 'VERB':  # type: ignore
            xcomp = t.children_with_ud_label('xcomp:pred')[0]
            xcomp.udep_label = 'obl'
            xcomp.ugov_id = t.gov2_id  # type: ignore
            xcomp.eud.clear()
            t.ugov = xcomp
            t.udep_label = 'case'
            t.upos = 'ADP'
            t.eud.clear()
        elif t.lemma == 'niech' and t.ugov and t.ugov.children_with_lemma('ż'):
            for child in t.ugov.children_with_lemma('ż'):
                child.ugov = t


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


def eud_correction(s: Sentence) -> None:
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
        # if t.gov_id != 0 and there are any 'root' relations in eud, remove  them
        if t.gov2_id != '0' and any(label == 'root' for label in t.data['eud'].values()):
            for gov in list(t.data['eud'].keys()):
                if t.data['eud'][gov] == 'root':
                    del t.data['eud'][gov]


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
