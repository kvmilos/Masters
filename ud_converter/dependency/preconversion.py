"""
Module for preprocessing dependency conversion from MPDT to UD.

This module handles preliminary adjustments to tokens before the main
dependency structure conversion takes place, such as correcting POS tags
based on syntactic context.
"""
from utils.logger import ChangeCollector
from utils.classes import Sentence


def preconversion(s: Sentence) -> None:
    """
    Performs preprocessing adjustments before dependency conversion.

    This function applies a series of rules to adjust token properties based
    on syntactic context, ensuring that the subsequent dependency conversion
    steps have the correct input. It handles cases like:
    1. Adding features to subordinating conjunctions in comparative constructions
    2. Correcting POS tags for auxiliary verbs that function as main verbs
    3. Ensuring proper identification of auxiliaries

    :param Sentence s: The sentence containing tokens to preprocess
    """
    for t in s.tokens:
        if not (t.upos == 'VERB' and t.dep_label == 'aux'):
            if (
                t.gov and t.upos == 'SCONJ'
                and t.lemma in ['jak', 'jakby']
                and t.dep_label == 'adjunct_compar'
            ):
                old_feats = t.ufeats.copy() if hasattr(t, 'ufeats') else None
                t.ufeats = {'ConjType': 'Comp'}
                ChangeCollector.record(t.sentence.id, t.id, f"ufeats changed from {old_feats} to {t.ufeats}", module="preconversion")

            elif (t.upos == 'AUX' and t.pos not in ['aglt', 'cond']
                  and t.dep_label != 'aux' and t.lemma not in ['to', 'by']
                  and len(t.children) > 0 and (not t.children_with_ud_label('conj') or len(t.children_with_ud_label('conj')) > 1)
                  and (not t.children_with_ud_label('cc') or len(t.children_with_ud_label('cc')) > 1)
            ):
                if (not t.children_with_label('pd') or len(t.children_with_label('pd')) > 1):
                    old_upos = t.upos
                    t.upos = 'VERB'
                    ChangeCollector.record(t.sentence.id, t.id, f"upos changed from {old_upos} to {t.upos}", module="preconversion")

            elif (t.upos == 'AUX' and t.pos not in ['aglt', 'cond']
                  and not t.children and t.lemma == 'być'
                  and t.dep_label not in ['aux', 'aglt']
            ):
                if t.super_gov_via_label('conjunct'):
                    if t.super_gov_via_label('conjunct')[1].dep_label != 'aux' and (not t.children_with_label('pd') or len(t.children_with_label('pd')) > 1): # type: ignore
                        old_upos = t.upos
                        t.upos = 'VERB'
                        ChangeCollector.record(t.sentence.id, t.id, f"upos changed from {old_upos} to {t.upos}", module="preconversion")
                else:
                    old_upos = t.upos
                    t.upos = 'VERB'
                    ChangeCollector.record(t.sentence.id, t.id, f"upos changed from {old_upos} to {t.upos}", module="preconversion")
