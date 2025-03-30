"""
Module for adjective POS-specific conversion.
"""

from utils.classes import Token
from utils.feats_dict import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn


def determiner(t: Token) -> None:
    """Converts a determiner."""
    t.upos = 'DET'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Degree': FU[t.feats['degree']]}


def adjective(t: Token) -> None:
    """Helper function for converting an adjective."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Degree': FU[t.feats['degree']]}


def adja(t: Token) -> None:
    """Converts an adja."""
    t.upos = 'ADJ'
    t.ufeats = {'Hyph': 'Yes'}


def adjb(t: Token) -> None:
    """Converts an adjb."""
    adjective(t)
    t.ufeats = {'Variant': 'Short'}


def adj(t: Token) -> None:
    """Converts an adj."""
    if not t.upos:
        if t.lemma in ['jaki', 'który']:
            determiner(t)
            t.ufeats = {'PronType': 'Int,Rel'}
        elif t.lemma in ['czyj', 'czyjże']:
            determiner(t)
            t.ufeats = {'PronType': 'Int'}
        elif t.lemma in ['któryż', 'jakiż']:
            determiner(t)
            t.ufeats = {'PronType': 'Emp'}
        elif t.lemma in ['któryś', 'którykolwiek', 'jakiś', 'jakikolwiek', 'niejaki', 'niektóry', 'niejeden', 'pewien']:
            determiner(t)
            t.ufeats = {'PronType': 'Ind'}
        elif t.lemma in ['każdy', 'wszelki', 'wszystek']:
            determiner(t)
            t.ufeats = {'PronType': 'Tot'}
        elif t.lemma in ['czyjś', 'czyjkolwiek']:
            determiner(t)
            t.ufeats = {'Poss': 'Yes'}
        elif t.lemma in ['żaden']:
            determiner(t)
            t.ufeats = {'PronType': 'Neg'}
        elif t.lemma in ['niczyj']:
            determiner(t)
            t.ufeats = {'Poss': 'Yes', 'PronType': 'Neg'}
        elif t.lemma in ['ten', 'tamten', 'ów', 'taki', 'takiż', 'tenże']:
            determiner(t)
            t.ufeats = {'PronType': 'Dem'}
        elif t.lemma in ['mój', 'twój', 'swój', 'nasz', 'wasz']:
            determiner(t)
            t.ufeats = {'Poss': 'Yes', 'PronType': 'Prs'}
            if t.lemma == 'mój':
                t.ufeats = {'Number[psor]': 'Sing', 'Person': '1'}
            elif t.lemma == 'twój':
                t.ufeats = {'Number[psor]': 'Sing', 'Person': '2'}
            elif t.lemma == 'swój':
                t.ufeats = {'Reflex': 'Yes'}
            elif t.lemma == 'nasz':
                t.ufeats = {'Number[psor]': 'Plur', 'Person': '1'}
            elif t.lemma == 'wasz':
                t.ufeats = {'Number[psor]': 'Plur', 'Person': '2'}
        else:
            adjective(t)
