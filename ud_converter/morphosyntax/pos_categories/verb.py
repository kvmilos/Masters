"""
Module for verb POS-specific conversion.

This module handles the conversion of various verb forms from the Middle Polish 
Dependency Treebank format to Universal Dependencies tags and features, including
different tenses, moods, aspects, and verbal forms.
"""
from utils.classes import Token
from utils.constants import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn


def fin(t: Token) -> None:
    """Converts a fin."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Voice': 'Act', 'Tense': 'Fut' if t.feats['aspect'] == 'perf' else 'Pres'}

def bedzie(t: Token) -> None:
    """Converts a bedzie."""
    t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Tense': 'Fut'}

def praet(t: Token) -> None:
    """Converts a praet."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    gn(t)
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Tense': 'Past', 'Voice': 'Act', 'Mood': 'Ind'}

def impt(t: Token) -> None:
    """Converts an impt."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Person': FU[t.feats['person']], 'Mood': 'Imp', 'Voice': 'Act', 'Number': FU[t.feats['number']]}

def imps(t: Token) -> None:
    """Converts an imps."""
    t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'Mood': 'Ind', 'Person': '0', 'Tense': 'Past', 'VerbForm': 'Fin', 'Voice': 'Act'}

def inf(t: Token) -> None:
    """Converts an inf."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Inf', 'Voice': 'Act'}

def ger(t: Token) -> None:
    """Converts a ger."""
    t.upos = 'NOUN'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']], 'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Pos', 'VerbForm': 'Vnoun'}

def pcon(t: Token) -> None:
    """Converts a pcon."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Conv', 'Voice': 'Act', 'Tense': 'Pres'}

def pant(t: Token) -> None:
    """Converts a pant."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Conv', 'Voice': 'Act', 'Tense': 'Past'}

def pact(t: Token) -> None:
    """Converts a pact."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']], 'Degree': FU[t.feats['degree']],
                'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Pos', 'VerbForm': 'Part', 'Voice': 'Act'}

def pactb(t: Token) -> None:
    """Converts a pactb."""
    pact(t)
    t.ufeats['Variant'] = 'Short'

def ppas(t: Token) -> None:
    """Converts a ppas."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']], 'Degree': FU[t.feats['degree']],
                'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Pos', 'VerbForm': 'Part', 'Voice': 'Pass'}

def ppasb(t: Token) -> None:
    """Converts a ppasb."""
    ppas(t)
    t.ufeats['Variant'] = 'Short'

def ppraet(t: Token) -> None:
    """Converts a ppraet."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']], 'Degree': FU[t.feats['degree']],
                'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Pos', 'VerbForm': 'Part', 'Voice': 'Pass'}

def fut(t: Token) -> None:
    """Converts a fut."""
    t.upos = 'AUX'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Tense': 'Fut'}

def plusq(t: Token) -> None:
    """Converts a plusq."""
    praet(t)

def aglt(t: Token) -> None:
    """Converts a aglt."""
    t.upos = 'AUX'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Variant': 'Long' if t.feats['vocalicity'] == 'wok' else 'Short'}

def winien(t: Token) -> None:
    """Converts a winien."""
    t.upos = 'VERB'
    gn(t)
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Tense': 'Pres',
                'Voice': 'Act', 'Mood': 'Ind', 'VerbType': 'Mod'}

def pred(t: Token) -> None:
    """Converts a pred."""
    if t.lemma == 'to':
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Mood': 'Ind', 'Tense': 'Pres', 'VerbForm': 'Fin', 'VerbType': 'Quasi'}
