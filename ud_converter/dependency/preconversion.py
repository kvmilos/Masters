"""
Module for the preconversion of the sentence.
"""
from utils.classes import Sentence


def preconversion(s: Sentence) -> None:
    """
    Preconversion of the sentence.
    """
    for t in s:
        if (t.gov and t.upos == 'SCONJ' and
        t.lemma in ['jak', 'jakby'] and
        t.dep_label == 'adjunct_compar'):
            t.ufeats = {'ConjType': 'Comp'}

        elif (t.upos == 'AUX' and t.pos not in ['aglt', 'cond'] and
        t.dep_label != 'aux' and t.lemma not in ['to', 'by'] and
        len(t.children) > 0 and not t.children_with_label('pd')):
            t.upos = 'VERB'

        elif (t.upos == 'AUX' and t.pos not in ['aglt', 'cond'] and
        not t.children and t.lemma == 'być' and
        t.dep_label not in ['aux', 'aglt', 'conjunct']):
            t.upos = 'VERB'

        elif (t.upos == 'AUX' and t.pos not in ['aglt', 'cond'] and
        not t.children and t.lemma == 'być' and
        t.dep_label not in ['aux', 'aglt'] and
        t.rec_gov_via_label('conjunct').dep_label != 'aux' and
        not t.gov.children_with_label('pd')):
            t.upos = 'VERB'

        elif t.upos == 'VERB' and t.dep_label == 'aux':
            t.upos = 'AUX'
