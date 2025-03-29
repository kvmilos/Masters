"""
Module for verb POS-specific conversion.
"""

from utils.classes import Token
from utils.feats_dict import FEATS_UPDATE as FU
from morphosyntax.helpers import update_gender_number as gn

def fin(t: Token):
    """Converts a fin."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Voice': 'Act', 'Tense': 'Fut' if t.feats['aspect'] == 'perf' else 'Pres'}

def bedzie(t: Token):
    """Converts a bedzie."""
    t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Tense': 'Fut'}

def praet(t: Token):
    """Converts a praet."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    gn(t)
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Tense': 'Past', 'Voice': 'Act', 'Mood': 'Ind'}

def impt(t: Token):
    """Converts an impt."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Person': FU[t.feats['person']], 'Mood': 'Imp', 'Voice': 'Act'}

def imps(t: Token):
    """Converts an imps."""
    t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'Mood': 'Ind', 'Person': '0', 'Tense': 'Past', 'VerbForm': 'Fin', 'Voice': 'Act'}

def inf(t: Token):
    """Converts an inf."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Inf', 'Voice': 'Act'}

def ger(t: Token):
    """Converts a ger."""
    t.upos = 'NOUN'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']], 'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Aff', 'VerbForm': 'Vnoun'}

def pcon(t: Token):
    """Converts a pcon."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Conv', 'Voice': 'Act', 'Tense': 'Pres'}

def pant(t: Token):
    """Converts a pant."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Conv', 'Voice': 'Act', 'Tense': 'Past'}

def pact(t: Token):
    """Converts a pact."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']],
                'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Aff', 'VerbForm': 'Part', 'Voice': 'Act'}

def pactb(t: Token):
    """Converts a pactb."""
    pact(t)
    t.ufeats['Variant'] = 'Short'

def ppas(t: Token):
    """Converts a ppas."""
    t.upos = 'ADJ'
    gn(t)
    t.ufeats = {'Case': FU[t.feats['case']], 'Aspect': FU[t.feats['aspect']],
                'Polarity': 'Neg' if t.feats['negation'] == 'neg' else 'Aff', 'VerbForm': 'Part', 'Voice': 'Pass'}

def ppasb(t: Token):
    """Converts a ppasb."""
    ppas(t)
    t.ufeats['Variant'] = 'Short'

def ppraet(t: Token):
    """Converts a ppraet."""
    if t.lemma in ['być', 'bywać']:
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    gn(t)
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Tense': 'Past', 'Voice': 'Act', 'Mood': 'Ind'}

def fut(t: Token):
    """Converts a fut."""
    t.upos = 'AUX'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Mood': 'Ind', 'Tense': 'Fut'}

def plusq(t: Token):
    """Converts a plusq."""
    praet(t)

def aglt(t: Token):
    """Converts a aglt."""
    t.upos = 'AUX'
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'Number': FU[t.feats['number']],
                'Person': FU[t.feats['person']], 'Variant': 'Long' if t.feats['vocalicity'] == 'wok' else 'Short'}

def agltaor(t: Token):
    """Converts a agltaor."""
    aglt(t)

def winien(t: Token):
    """Converts a winien."""
    t.upos = 'VERB'
    gn(t)
    t.ufeats = {'Aspect': FU[t.feats['aspect']], 'VerbForm': 'Fin', 'Tense': 'Pres',
                'Voice': 'Act', 'Mood': 'Ind', 'VerbType': 'Mod'}

def pred(t: Token):
    """Converts a pred."""
    if t.lemma == 'to':
        t.upos = 'AUX'
    else:
        t.upos = 'VERB'
    t.ufeats = {'Mood': 'Ind', 'Tense': 'Pres', 'VerbForm': 'Fin', 'VerbType': 'Quasi'}
