"""
Module for pronoun POS-specific conversion.
"""

from utils.classes import Token
from utils.feats_dict import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn


def ppron(t: Token):
    """Helper function for converting a personal pronoun."""
    t.upos = 'PRON'
    t.ufeats = {'PronType': 'Prs', 'Case': FU[t.feats['case']], 'Person': FU[t.feats['person']]}


def ppron12(t: Token):
    """Converts a ppron12."""
    ppron(t)
    t.ufeats = {'Number': FU[t.feats['number']]}
    if t.feats['accentability'] == 'akc':
        t.ufeats = {'Variant': 'Long'}
    else:
        t.ufeats = {'Variant': 'Short'}


def ppron3(t: Token):
    """Converts a ppron3."""
    ppron(t)
    gn(t)
    t.ufeats = {'PrepCase': FU[t.feats['post-prepositionality']]}
    if t.feats['accentability'] == 'akc':
        t.ufeats = {'Variant': 'Long'}
    else:
        t.ufeats = {'Variant': 'Short'}


def siebie(t: Token):
    """Converts a siebie."""
    t.upos = 'PRON'
    t.ufeats = {'PronType': 'Prs', 'Reflex': 'Yes', 'Case': FU[t.feats['case']]}
