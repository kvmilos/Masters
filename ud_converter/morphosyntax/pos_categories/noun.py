"""
Module for noun POS-specific conversion.
"""
from utils.classes import Token
from utils.constants import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn


def subst(t: Token) -> None:
    """Converts a subst."""
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']]}
    if not t.upos:
        if t.lemma in ['co', 'kto']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Int,Rel'}
        elif t.lemma in ['któż', 'cóż']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Int'}
        elif t.lemma in ['ktoś', 'ktokolwiek', 'coś', 'cokolwiek']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Ind'}
        elif t.lemma in ['nikt', 'nic']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Neg'}
        elif t.lemma in ['to', 'tamto']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Dem'}
        elif t.lemma in ['wszyscy', 'wszystko']:
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Tot'}
        else:
            t.upos = 'NOUN'
