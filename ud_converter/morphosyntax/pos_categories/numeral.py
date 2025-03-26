"""
Module for numerals POS-specific conversion.
"""

from utils.classes import Token
from utils.feats_dict import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn
from morphosyntax.pos_categories.adjective import adj
from morphosyntax.pos_categories.adverb import adv



def numeral(t: Token):
    """Converts a num or numcol."""
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']]}
    if not t.upos:
        if t.lemma in ['ile', 'ileż', 'iluż']:
            t.upos = 'DET'
            t.ufeats = {'NumType': 'Card', 'PronType': 'Int'}
        elif t.lemma in ['tyle', 'tyleż']:
            t.upos = 'DET'
            t.ufeats = {'NumType': 'Card', 'PronType': 'Dem'}
        elif t.lemma in ['mało', 'niemało', 'mniej', 'najmniej', 'dużo', 'niedużo', 'wiele', 'niewiele', 'więcej', 'najwięcej', 'kilka', 'kilkanaście', 'kilkadziesiąt', 'kilkaset', 'parę', 'paręnaście', 'oba', 'parędziesiąt', 'nieco', 'sporo', 'trochę', 'ileś', 'ilekolwiek', 'pełno', 'dość', 'dosyć']:
            t.upos = 'DET'
            t.ufeats = {'NumType': 'Card', 'PronType': 'Ind'}
        else:
            t.upos = 'NUM'
            t.ufeats = {'NumForm': 'Word'}


def adjnum(t: Token):
    """Converts an adjnum."""
    adj(t)
    t.ufeats = {'NumType': 'Ord'}


def advnum(t: Token):
    """Converts an advnum."""
    adv(t)
    t.ufeats = {'NumType': 'Ord'}
