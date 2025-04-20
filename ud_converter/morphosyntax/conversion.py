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
from morphosyntax.pos_categories.other import brev, frag, interj, part, prep, conj, comp, interp, xxx, dig, romandig, ign, sym, incert

MODULE_PREFIX = f"ud_converter.{__name__}"


def pos_specific_upos(t: Token) -> None:
    """
    Applies the conversion to UPOS based on the token's part of speech (POS).

    This function acts as a dispatcher that routes each token to the appropriate
    conversion function based on its original POS tag. It handles all POS categories
    defined in the MPDT tagset.

    :param Token t: The token to be converted
    """
    converter_func = None
    if t.upos == '':
        if t.pos == 'subst':
            converter_func = subst
            converter_func(t)
        elif t.pos == 'adj':
            converter_func = adj
            converter_func(t)
        elif t.pos == 'adja':
            converter_func = adja
            converter_func(t)
        elif t.pos == 'adjb':
            converter_func = adjb
            converter_func(t)
        elif t.pos == 'adv':
            converter_func = adv
            converter_func(t)
        elif t.pos in ['num', 'numcol']:
            converter_func = numeral
            converter_func(t)
        elif t.pos == 'adjnum':
            converter_func = adjnum
            converter_func(t)
        elif t.pos == 'advnum':
            converter_func = advnum
            converter_func(t)
        elif t.pos == 'fin':
            converter_func = fin
            converter_func(t)
        elif t.pos == 'bedzie':
            converter_func = bedzie
            converter_func(t)
        elif t.pos == 'praet':
            converter_func = praet
            converter_func(t)
        elif t.pos == 'impt':
            converter_func = impt
            converter_func(t)
        elif t.pos == 'imps':
            converter_func = imps
            converter_func(t)
        elif t.pos == 'inf':
            converter_func = inf
            converter_func(t)
        elif t.pos == 'ger':
            converter_func = ger
            converter_func(t)
        elif t.pos == 'pcon':
            converter_func = pcon
            converter_func(t)
        elif t.pos == 'pant':
            converter_func = pant
            converter_func(t)
        elif t.pos == 'pact':
            converter_func = pact
            converter_func(t)
        elif t.pos == 'pactb':
            converter_func = pactb
            converter_func(t)
        elif t.pos == 'ppas':
            converter_func = ppas
            converter_func(t)
        elif t.pos == 'ppasb':
            converter_func = ppasb
            converter_func(t)
        elif t.pos == 'ppraet':
            converter_func = ppraet
            converter_func(t)
        elif t.pos == 'fut':
            converter_func = fut
            converter_func(t)
        elif t.pos == 'plusq':
            converter_func = plusq
            converter_func(t)
        elif t.pos in ['aglt', 'agltaor']:
            converter_func = aglt
            converter_func(t)
        elif t.pos == 'winien':
            converter_func = winien
            converter_func(t)
        elif t.pos == 'pred':
            converter_func = pred
            converter_func(t)
        elif t.pos == 'frag':
            converter_func = frag
            converter_func(t)
        elif t.pos == 'interj':
            converter_func = interj
            converter_func(t)
        elif t.pos == 'part':
            converter_func = part
            converter_func(t)
        elif t.pos == 'prep':
            converter_func = prep
            converter_func(t)
        elif t.pos == 'brev':
            converter_func = brev
            converter_func(t)
        elif t.pos == 'conj':
            converter_func = conj
            converter_func(t)
        elif t.pos == 'comp':
            converter_func = comp
            converter_func(t)
        elif t.pos == 'ppron12':
            converter_func = ppron12
            converter_func(t)
        elif t.pos == 'ppron3':
            converter_func = ppron3
            converter_func(t)
        elif t.pos == 'siebie':
            converter_func = siebie
            converter_func(t)
        elif t.pos == 'interp':
            converter_func = interp
            converter_func(t)
        elif t.pos == 'xxx':
            converter_func = xxx
            converter_func(t)
        elif t.pos == 'dig':
            converter_func = dig
            converter_func(t)
        elif t.pos == 'romandig':
            converter_func = romandig
            converter_func(t)
        elif t.pos == 'ign':
            converter_func = ign
            converter_func(t)
        elif t.pos == 'sym':
            converter_func = sym
            converter_func(t)
        elif t.pos == 'incert':
            converter_func = incert
            converter_func(t)
        else:
            # log unrecognised POS under 'conversion' category with padded prefix
            warning_logger = logging.getLogger(MODULE_PREFIX + '.conversion')
            warning_logger.warning(
                "S%-5s T%-5s- Unrecognised part of speech >>%s<< for token >>%s<< in sentence: %s",
                t.sentence.id, t.id, t.pos, t.form,
                t.sentence.text if t.sentence else 'unknown'
            )
    # after conversion, only log if a specific conversion function ran
    if converter_func:
        category = converter_func.__module__.split('.')[-1]
        category_logger = logging.getLogger(f"{MODULE_PREFIX}.{category}")
        category_logger.debug(
            "S%-5s T%-5s- Converted %s to %s",
            t.sentence.id, t.id, t.form, t.upos
        )
