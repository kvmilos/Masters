"""
Module for adverb POS-specific conversion.
"""
from utils.classes import Token
from utils.constants import FEATS_UPDATE as FU


def adv(t: Token) -> None:
    """Converts an adv."""
    t.upos = 'ADV'
    if (
        t.lemma == 'jak'
        and t.dep_label == 'adjunct_compar'
        and t.children_with_pos('fin')
    ):
        t.upos = 'SCONJ'
        t.ufeats = {'ConjType': 'Comp'}
    elif 'degree' in t.feats:
        t.ufeats = {'Degree': FU[t.feats['degree']]}
    if t.lemma in ['kiedy', 'gdzie']:
        if t.prev and t.prev.lemma == 'rzadko':
            pass
        elif t.next and t.next.lemma == 'indziej':
            pass
        else:
            t.ufeats = {'PronType': 'Int,Rel'}
    elif t.lemma == 'jak':
        if not t.next or 'degree' in t.next.feats and t.next.feats['degree'] != 'sup':
            t.ufeats = {'PronType': 'Int,Rel'}
    elif t.lemma == 'ile':
        if not t.prev or t.prev.lemma != 'o':
            t.ufeats = {'PronType': 'Int,Rel'}
    elif t.lemma in ['tak', 'tu', 'tutaj', 'tam', 'ówdzie', 'stąd', 'stamtąd', 'tędy', 'tamtędy', 'wtedy', 'wówczas', 'wtenczas', 'odtąd', 'dotąd', 'dlatego']:
        t.ufeats = {'PronType': 'Dem'}
    elif t.lemma in ['dokąd', 'skąd', 'jakkolwiek', 'gdziekolwiek', 'kiedykolwiek', 'którędykolwiek', 'niekiedy', 'gdzieniegdzie']:
        t.ufeats = {'PronType': 'Ind'}
    elif t.lemma in ['nigdy', 'nigdzie']:
        t.ufeats = {'PronType': 'Neg'}
    elif t.lemma in ['zawsze', 'wszędzie', 'zewsząd']:
        t.ufeats = {'PronType': 'Tot'}
    elif t.lemma in ['dlaczego', 'czemu', 'odkąd', 'którędy', 'dlaczegoż', 'dlaczegóż', 'czemuż', 'dokądże', 'skądże', 'jakże', 'którędyż', 'gdzież', 'kiedyż']:
        t.ufeats = {'PronType': 'Int'}
