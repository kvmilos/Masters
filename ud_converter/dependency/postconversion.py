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
    default_ugov(s)
    unit_fixes(s)
    fix_fixed(s)
    fix_det_child(s)
    fix_order(s)
    fix_mark(s)
    mpdt_2000_specific_fixes(s)  # MPDT_2000 specific! Delete if using another corpus
    remove_numtype_adv_kroc(s)
    add_extpos(s)
    delete_punct_children(s)
    delete_cc_children(s)
    complete_eud(s)
    fix_num(s)
    fix_advmod(s)
    delete_mark_children(s)
    ufeats_correction(s)
    eud_correction(s)


def default_ugov(s: Sentence) -> None:
    """
    Sets the gov -> ugov for tokens that don't have a ugov.
    """
    for t in s.tokens:
        if '-' not in t.id:
            if t.ugov_id == '_':
                # If the enhanced governor ID is '_', set it to the basic governor ID
                t.ugov_id = t.gov_id
                ChangeCollector.record(t.sentence.id, t.id, f"Setting gov -> ugov ({t.gov_id}) for token: '{t.form}'", module="postconversion1")


def remove_numtype_adv_kroc(s: Sentence) -> None:
    """
    Removes the 'NumType=Ord' feature from ADV ending in -kroć
    """
    for t in s.tokens:
        if t.upos == 'ADV' and t.lemma.endswith('kroć'):
            t.ufeats.pop('NumType', None)
            ChangeCollector.record(t.sentence.id, t.id, f"Removing 'NumType=Ord' from token: '{t.form}'", module="postconversion2")


def fix_advmod(s: Sentence) -> None:
    """
    Fixes the UPOS of tokens with 'advmod' dependency label UPOS.
    """
    for t in s.tokens:
        if t.udep_label.startswith('advmod') and t.upos == 'NOUN':
            if t.lemma == 'ni':
                t.upos = 'ADV'
                t.feats.clear()
            elif [c for c in t.children2 if c.udep_label == 'case']:
                t.udep_label = 'obl'
        elif t.pos.startswith('inf') and t.next and t.next.lemma == 'by' and t.next.upos == 'AUX' and t.next.gov2 and t.next.gov2.upos == 'NOUN':
            t.next.ugov = t
            t.next.upos = 'SCONJ'
            t.next.udep_label = 'mark'
        elif t.lemma == 'sam' and t.next and t.next.lemma == 'przez' and t.next.next and t.next.next.lemma == 'się':
            t.next.ugov = t
            t.next.udep_label = 'fixed'
            t.next.next.ugov = t
            t.next.next.udep_label = 'fixed'
            t.ufeats['ExtPos'] = 'ADV'
        elif t.udep_label.startswith('advmod') and t.upos == 'PRON' and t.lemma == 'to' and [c for c in t.children2 if c.udep_label == 'case']:
            t.udep_label = 'obl'


def fix_num(s: Sentence) -> None:
    """
    Changes the UPOS of tokens with 'dig' POS and 'X' UPOS to 'NUM'.
    """
    for t in s.tokens:
        if t.pos == 'dig':
            t.upos = 'NUM'
            ChangeCollector.record(t.sentence.id, t.id, f"Changing UPOS from 'X' to 'NUM' for token: '{t.form}'", module="postconversion3")


def fix_fixed(s: Sentence) -> None:
    """
    Fixes some 'fixed' dependency labels in a sentence.
    """
    for t in s.tokens:
        if t.children_with_ud_label('fixed'):
            if t.pos.startswith('brev'):
                for child in t.children_with_ud_label('fixed'):
                    child.udep_label = 'flat'
            elif t.pos != 'dig' and any(child.pos.startswith('brev') for child in t.children_with_ud_label('fixed')):
                for child in t.children_with_ud_label('fixed'):
                    if child.pos.startswith('brev'):
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
                newgov = gov.gov2.children_with_ud_label('amod')[0]  # type: ignore
                t.ugov = child
                gov.ugov = child
                child.ugov = newgov
                child.udep_label = 'obl'
            elif t.upos == 'PUNCT' and t.gov2 and t.gov2.upos == 'X' and t.children_with_ud_label('fixed')[0].upos == 'X':  # type: ignore
                child = t.children_with_ud_label('fixed')[0]
                t.udep_label = 'punct'
                child.udep_label = 'flat'
                child.ugov = t.gov2
            elif t.pos == 'conj' and t.next and t.next.upos == 'NUM' and t.gov2 and t.gov2.upos == 'NUM':
                gov = t.gov2
                num = t.next
                t.udep_label = 'cc'
                num.ugov = gov
                num.udep_label = 'conj'
            # elif t.lemma == 'milion' and t.children_with_ud_label('fixed')[0].lemma == 'milion':
            #     child = t.children_with_ud_label('fixed')[0]
            #     t.upos = 'NUM'
            #     child.upos = 'NUM'
            #     t.udep_label = 'nummod'
            #     child.udep_label = 'flat'
            #     gov_list = t.children_with_ud_label('nmod:arg')
            #     if gov_list and t.gov2:
            #         gov = gov_list[0]
            #         gov.ugov = t.gov2
            #         t.ugov = gov
            #         gov.udep_label = 'nmod:tmod'
            elif t.lemma in ['sto', 'tysiąc', 'milion'] and t.children_with_ud_label('fixed')[0].lemma in ['sto', 'tysiąc', 'milion']:
                t.children_with_ud_label('fixed')[0].udep_label = 'flat'
            elif [c for c in t.children2 if c.form.lower() == t.form.lower() and c.udep_label == 'fixed']:
                for c in t.children2:
                    if c.form.lower() == t.form.lower() and c.udep_label == 'fixed' and t.next and t.next.lemma == 'nie' and t.next.gov2 == c:
                        c.udep_label = 'flat'


def fix_mark(s: Sentence) -> None:
    """
    Fixes problems with 'mark'
    """
    for t in s.tokens:
        if t.udep_label == 'mark_rel' and t.lemma == 'co':
            t.upos = 'PART'
            t.ufeats.clear()
        elif t.udep_label == 'mark' and t.upos == 'DET':
            t.udep_label = 'det'


def delete_mark_children(s: Sentence) -> None:
    """
    Deletes children of tokens with 'mark' dependency label.
    """
    for t in s.tokens:
        if t.udep_label == 'mark' and t.children2 and [c for c in t.children2 if c.lemma == 'by']:
            for c in t.children2:
                if c.lemma == 'by' and c.upos == 'AUX':
                    c.upos = 'PART'
        elif t.udep_label == 'mark' and t.uchildren and t.gov2:
            for c in t.uchildren:
                if c.udep_label != 'fixed':
                    c.ugov = t.gov2


def delete_punct_children(s: Sentence) -> None:
    """
    Deletes children of tokens with 'punct' dependency label.
    """
    for t in s.tokens:
        if t.udep_label == 'punct' and t.children2 and t.gov2:
            for c in t.children2:
                if c.upos != 'PUNCT':
                    c.ugov = t.gov2
                    if t.id in c.eud:
                        del c.eud[t.id]


def delete_cc_children(s: Sentence) -> None:
    """
    Deletes children of tokens with 'cc' dependency label.
    """
    for t in s.tokens:
        if t.udep_label == 'cc' and t.children2 and t.gov2:
            for c in t.children2:
                if c.upos not in ['PART', 'CCONJ', 'SCONJ', 'ADV']:
                    c.ugov = t.gov2
                    if t.id in c.eud:
                        del c.eud[t.id]


def fix_det_child(s: Sentence) -> None:
    """
    Fixes [L3 Syntax leaf-det] 'det' not expected to have children error.
    """
    for t in s.tokens:
        if t.udep_label != 'det' or not t.uchildren or t.lemma == 'pewien':
            continue
        for child in t.uchildren:
            if child.udep_label in ['fixed', 'flat'] or child.udep_label.startswith('advmod') or child.udep_label.startswith('obl'):
                continue
            if t.ugov and child.upos != 'PART':
                child.ugov = t.ugov


def fix_order(s: Sentence) -> None:
    """
    Fixes the order of conjuncts in a sentence.
    """
    for t in s.tokens:
        if t.udep_label == 'conj' and t.gov2 and int(t.gov2.id) > int(t.id):
            old_label = t.gov2.udep_label
            old_gov = t.gov2.gov2_id
            t.gov2.udep_label = 'conj'
            t.gov2.ugov = t
            t.gov2.eud.clear()
            t.ugov_id = old_gov
            t.udep_label = old_label
            for t2 in s.tokens:
                if t2.gov2 and t2.gov2.id == t.gov2.id and t2.udep_label == 'conj':
                    t2.ugov = t
                if t2.eud and t.gov2.id in t2.eud and t2.eud[t.gov2.id] == 'conj':
                    del t2.eud[t.gov2.id]
                    t2.eud = {t.id: 'conj'}
        if t.udep_label in ['fixed', 'flat'] and t.gov2 and int(t.gov2.id) > int(t.id):
            old_label = t.gov2.udep_label
            old_gov = t.gov2.gov2_id
            t.gov2.udep_label = t.udep_label
            t.gov2.ugov = t
            t.ugov_id = old_gov
            t.udep_label = old_label
            t.eud = t.gov2.eud.copy() if t.gov2 and t.gov2.eud else {}
            t.gov2.eud.clear()


def mpdt_2000_specific_fixes(s: Sentence) -> None:
    """
    Corrects unit errors in punctuation tokens and some other specific fixes
    for the MPDT_2000 corpus.
    """
    if s.id == '43':
        for t in s.tokens:
            if t.id == '18':
                t.ugov_id = '17'
    elif s.id == '239':
        for t in s.tokens:
            if t.id == '6':
                t.ugov_id = '5'
            elif t.id == '13':
                t.ugov_id = '12'
    elif s.id == '831':
        for t in s.tokens:
            if t.id == '2':
                t.ugov_id = '3'
    elif s.id == '1132':
        for t in s.tokens:
            if t.id == '15':
                t.ugov_id = '13'
    elif s.id == '1855':
        for t in s.tokens:
            if t.id == '8':
                t.ugov_id = '10'
    elif s.id == '1596':
        for t in s.tokens:
            if t.id == '6':
                t.ugov_id = '0'
                t.udep_label = 'root'
                t.data['eud'].clear()
            elif t.id == '7':
                t.ugov_id = '6'
            elif t.id == '10' or t.id == '13':
                t.ugov_id = '6'
                t.data['eud'].clear()
                t.data['eud']['6'] = 'conj'
            elif t.id == '17':
                t.ugov_id = '6'
    for t in s.tokens:
        if t.upos == 'PUNCT' and t.udep_label != 'punct':
            t.udep_label = 'punct'
    if s.id == '1757':
        for t in s.tokens:
            if t.id == '5':
                t.udep_label = 'flat'
    elif s.id == '942':
        for t in s.tokens:
            if t.id == '37':
                t.udep_label = 'flat'
    elif s.id == '536':
        for t in s.tokens:
            if t.id == '5':
                t.udep_label = 'flat'
    elif s.id == '484':
        for t in s.tokens:
            if t.id == '10':
                t.udep_label = 'case'
                t.ugov_id = '11'
            elif t.id == '11':
                t.udep_label = 'obl'
            elif t.id == '12':
                t.udep_label = 'obl:arg'
    elif s.id == '755':
        for t in s.tokens:
            if t.id == '29':
                t.udep_label = 'obl'
                t.ugov_id = '33'
            elif t.id == '33':
                t.ugov_id = '18'
    elif s.id == '1202':
        for t in s.tokens:
            if t.id == '5':
                t.udep_label = 'obj'
                t.upos = 'NOUN'
            elif t.id == '11':
                t.upos = 'NOUN'
                t.ugov_id = '5'
            elif t.id == '17':
                t.ugov_id = '5'
                t.udep_label = 'conj'
                t.upos = 'NOUN'
            elif t.id in ['7', '13', '19']:
                t.udep_label = 'nummod'
            elif t.id == '8':
                t.ugov_id = '7'
            elif t.id == '14':
                t.ugov_id = '13'
            elif t.id == '20':
                t.ugov_id = '19'
            elif t.id == '9':
                t.ugov_id = '7'
            elif t.id == '15':
                t.ugov_id = '13'
            elif t.id == '21':
                t.ugov_id = '19'
            elif t.id in ['10', '16', '22']:
                t.ugov = t.next # type: ignore
    elif s.id == '319':
        for t in s.tokens:
            if t.id == '14':
                t.ugov_id = '2'
                t.udep_label = 'conj'
    elif s.id == '501':
        for t in s.tokens:
            if t.id == '6':
                t.udep_label = 'nummod'
    elif s.id == '633':
        for t in s.tokens:
            if t.id in ['1', '3', '4']:
                t.ugov_id = '5'
            elif t.id == '5':
                t.ugov_id = '0'
                t.udep_label = 'root'
            elif t.id == '8':
                t.ugov_id = '5'
                t.udep_label = 'ccomp'
    elif s.id == '689':
        for t in s.tokens:
            if t.id == '33':
                t.udep_label = 'flat'
    elif s.id == '661':
        for t in s.tokens:
            if t.id in ['4', '6']:
                t.ugov_id = '2'
    elif s.id == '999':
        for t in s.tokens:
            if t.id == '10':
                t.ugov_id = '8'
    elif s.id == '1205':
        for t in s.tokens:
            if t.id == '3':
                t.ugov_id = '5'
    elif s.id == '983':
        for t in s.tokens:
            if t.id == '4':
                t.udep_label = 'nsubj:outer'
    elif s.id == '1222':
        for t in s.tokens:
            if t.id == '14':
                t.udep_label = 'nsubj:outer'
    elif s.id == '1702':
        for t in s.tokens:
            if t.id == '18':
                t.ugov_id = '14'
    elif s.id == '199':
        for t in s.tokens:
            if t.id == '23':
                t.ufeats.clear()
    elif s.id == '1011':
        for t in s.tokens:
            if t.id == '2':
                t.udep_label = 'flat'


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
    # open once per sentence
    for t in s.tokens:
        fixed_children = t.children_with_ud_label('fixed')
        if not fixed_children:
            continue

        # set the ExtPos feature
        t.ufeats = {'ExtPos': extpos(t, t.children_with_ud_label('fixed'))}


def extpos(t: Token, ch: list[Token]) -> str:
    """
    Determines the external part-of-speech tag for a token and child(ren).

    :param Token token: The token to analyze
    :param list[Token] fixed_children: The fixed children of the token
    :return: The external part-of-speech tag
    :rtype: str
    """
    # if len(ch) > 1:
    #     print(f'LOL {t.sentence.id} {t.form} {[c.form for c in ch]}')
    c = ch[0]
    if t.lemma == 'dla' and c.form == 'tego':
        return 'ADV'
    if t.lemma in ['wraz', 'razem'] and c.lemma in ['z', 'ze']:
        return 'ADP'
    if t.upos == 'ADP' and t.udep_label.startswith('advmod'):
        return 'ADV'
    if c.lemma == 'i':
        if t.lemma == 'jako' and t.upos == 'CCONJ':
            t.upos = 'SCONJ'
            return 'SCONJ'
        return 'CCONJ'
    if t.upos == 'DET' and t.ufeats['Case'] == 'Ins' and c.upos == 'NOUN':
        return 'ADV'
    if t.upos == 'PART' and c.upos == 'ADV':
        return 'ADV'
    if t.lemma == 'to' and t.upos == 'PART' and c.lemma == 'być' and c.upos == 'VERB' and t.udep_label == 'advmod:emph':
        return 'CCONJ'
    if t.lemma == 'za' and c.form == 'czym':
        return 'SCONJ'
    if t.lemma == 'a' and c.lemma in ['mianowicie', 'niżeli']:
        return 'CCONJ'
    if t.lemma == 'jednak' and c.lemma == 'że':
        return 'CCONJ'
    if t.upos in ['DET', 'PRON', 'NOUN'] and c.upos in ['DET', 'PRON', 'NOUN'] and t.form.istitle() and c.form.istitle():
        return 'PROPN'
    if t.lemma == 'gdy' and c.lemma == 'by':
        return 'SCONJ'
    if t.lemma == 'czy' and c.lemma == 'to':
        return 'SCONJ'
    if t.lemma == 'jako' and c.lemma == 'to' and t.udep_label.startswith('adv'):
        return 'ADV'
    if t.lemma == 'jako' and t.upos in ['ADP', 'PART'] and c.lemma == 'to' and c.upos == 'PART':
        return 'SCONJ'
    if t.lemma == 'sam' and c.lemma == 'przez' and ch[1].lemma == 'się':
        return 'ADV'
    if t.lemma == 'co' and c.lemma == 'do':
        return 'ADP'
    if t.lemma == 'jednak' and t.upos == 'PART' and c.lemma == 'ż' and c.upos == 'PART':
        return 'CCONJ'
    if t.lemma == 'nie' and c.lemma == 'tylko':
        return 'CCONJ'
    if t.lemma == 'czy' and c.lemma == 'li' and c.next and c.next.lemma == 'ż':
        return 'ADV'
    if t.upos == 'X':
        return c.upos
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
                child.udep_label = 'fixed'
        elif t.form in ['ż', 'ć'] and t.gov2 and t.udep_label == 'fixed' and t.upos == 'PART':
            t.udep_label = 'advmod:emph'

def ufeats_correction(s: Sentence) -> None:
    """
    Corrects the ufeats dictionary for each token in the sentence.
    """
    for t in s.tokens:
        if 'Case' in t.ufeats and t.ufeats['Case'] == '':
            # If the Case feature is empty, remove it
            del t.ufeats['Case']
            ChangeCollector.record(t.sentence.id, t.id, f"Removed empty 'Case' feature for token: '{t.form}'", module="postconversion")


def complete_eud(s: Sentence) -> None:
    """
    Completes the enhanced dependency graph for a sentence.

    :param Sentence s: The sentence to process
    """
    for t in s.tokens:
        if '-' not in t.id:
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
