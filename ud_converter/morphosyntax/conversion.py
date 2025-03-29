"""
Module responsible for the POS-specific conversion to UPOS.
"""

import logging
from utils.classes import Token
from morphosyntax.pos_categories.noun import subst
from morphosyntax.pos_categories.adjective import adj, adja, adjb
from morphosyntax.pos_categories.adverb import adv
from morphosyntax.pos_categories.numeral import numeral, adjnum, advnum
from morphosyntax.pos_categories.pronoun import ppron12, ppron3, siebie
from morphosyntax.pos_categories.other import brev, frag, interj, part, prep, conj, comp, interp, xxx, dig, romandig, ign, sym, incert

logger = logging.getLogger('ud_converter.morphosyntax.conversion')

def pos_specific_upos(t: Token):
    """
    Applies the conversion based on the POS.
    """
    if t.pos == 'subst':
        subst(t)
    elif t.pos == 'adj':
        adj(t)
    elif t.pos == 'adja':
        adja(t)
    elif t.pos == 'adjb':
        adjb(t)
    elif t.pos == 'adv':
        adv(t)
    elif t.pos in ['num', 'numcol']:
        numeral(t)
    elif t.pos == 'adjnum':
        adjnum(t)
    elif t.pos == 'advnum':
        advnum(t)
    elif t.pos == 'brev':
        brev(t)
    elif t.pos == 'frag':
        frag(t)
    elif t.pos == 'interj':
        interj(t)
    elif t.pos == 'part':
        part(t)
    elif t.pos == 'prep':
        prep(t)
    elif t.pos == 'conj':
        conj(t)
    elif t.pos == 'comp':
        comp(t)
    elif t.pos == 'ppron12':
        ppron12(t)
    elif t.pos == 'ppron3':
        ppron3(t)
    elif t.pos == 'siebie':
        siebie(t)
    elif t.pos == 'interp':
        interp(t)
    elif t.pos == 'xxx':
        xxx(t)
    elif t.pos == 'dig':
        dig(t)
    elif t.pos == 'romandig':
        romandig(t)
    elif t.pos == 'ign':
        ign(t)
    elif t.pos == 'sym':
        sym(t)
    elif t.pos == 'incert':
        incert(t)
    else:
        logger.warning('Unrecognised part of speech >>%s<< of the token >>%s<< in >>%s<<', t.pos, t.form, t.sentence.text)
    logger.debug('Converted %s to %s', t.form, t.upos)
