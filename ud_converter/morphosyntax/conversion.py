"""
Module responsible for the POS-specific conversion to UPOS tags.

This module contains the main conversion function that delegates the conversion
process to appropriate handlers based on the token's original part of speech (POS).
Each POS category has its own specific conversion function imported from the
pos_categories subpackage.
"""
import logging
from utils.classes import Token
from morphosyntax.pos_categories.noun import subst
from morphosyntax.pos_categories.adjective import adj, adja, adjb
from morphosyntax.pos_categories.adverb import adv
from morphosyntax.pos_categories.numeral import numeral, adjnum, advnum
from morphosyntax.pos_categories.pronoun import ppron12, ppron3, siebie
from morphosyntax.pos_categories.verb import fin, bedzie, praet, impt, imps, inf, ger, pcon, pant, pact, pactb, ppas, ppasb, ppraet, fut, plusq, aglt, winien, pred
from morphosyntax.pos_categories.other import brev, frag, interj, part, prep, conj, comp,interp, xxx, dig, romandig, ign, sym, incert

logger = logging.getLogger('ud_converter.morphosyntax.conversion')


def pos_specific_upos(t: Token) -> None:
    """
    Applies the conversion to UPOS based on the token's part of speech (POS).

    This function acts as a dispatcher that routes each token to the appropriate
    conversion function based on its original POS tag. It handles all POS categories
    defined in the MPDT tagset.

    :param Token t: The token to be converted
    """
    if t.upos == '':
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
        elif t.pos == 'fin':
            fin(t)
        elif t.pos == 'bedzie':
            bedzie(t)
        elif t.pos == 'praet':
            praet(t)
        elif t.pos == 'impt':
            impt(t)
        elif t.pos == 'imps':
            imps(t)
        elif t.pos == 'inf':
            inf(t)
        elif t.pos == 'ger':
            ger(t)
        elif t.pos == 'pcon':
            pcon(t)
        elif t.pos == 'pant':
            pant(t)
        elif t.pos == 'pact':
            pact(t)
        elif t.pos == 'pactb':
            pactb(t)
        elif t.pos == 'ppas':
            ppas(t)
        elif t.pos == 'ppasb':
            ppasb(t)
        elif t.pos == 'ppraet':
            ppraet(t)
        elif t.pos == 'fut':
            fut(t)
        elif t.pos == 'plusq':
            plusq(t)
        elif t.pos in ['aglt', 'agltaor']:
            aglt(t)
        elif t.pos == 'winien':
            winien(t)
        elif t.pos == 'pred':
            pred(t)
        elif t.pos == 'frag':
            frag(t)
        elif t.pos == 'interj':
            interj(t)
        elif t.pos == 'part':
            part(t)
        elif t.pos == 'prep':
            prep(t)
        elif t.pos == 'brev':
            brev(t)
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
            logger.warning("Sentence %s: Unrecognised part of speech >>%s<< of the token >>%s<< in >>%s<<", t.sentence.id, t.pos, t.form, t.sentence.text if t.sentence else 'unknown')
        logger.debug("Sentence %s: Converted %s to %s", t.sentence.id, t.form, t.upos)
