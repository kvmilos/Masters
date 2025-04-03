"""
Module for labels conversion.
"""
import logging
from utils.classes import Token
from utils.constants import PARTICLES
logger = logging.getLogger('ud_converter.dependency.labels')


def convert_label(t: Token) -> str:
    """
    Converts the dependency label to the UD format and returns it.
    """
    if t.udep_label != '_':
        return t.udep_label

    # discourse element (emoji)
    if t.pos == 'sym' and t.dep_label == 'adjunct_comment':
        return 'discourse'
    # discourse element (interjection)
    elif t.pos == 'interj' and t.dep_label != 'root':
        return 'discourse:intj'
    # subordinating conjunction
    elif t.lemma == 'o' and t.children_with_lemma('tyle') == 1 and t.children_with_lemma('tyle')[0].dep_label == 'mwe':
        return 'mark'
    elif t.lemma == 'o' and t.children_with_lemma('tyle') > 1:
        logger.warning('Multiple "tyle"-lemma children for o: %s', t.form)
    # possessive determiner or determiner
    elif t.upos == 'DET' and t.pos != 'num' and t.dep_label in ['adjunct', 'poss']:
        if t.ufeats['Poss'] == 'Yes':
            return 'det:poss'
        else:
            return 'det'
    # passive auxiliary or auxiliary
    elif t.dep_label == 'aux':
        if t.governor and t.governor.pos == 'ppas':
            return 'aux:pass'
        else:
            return 'aux'
    # vocative
    elif t.dep_label == 'vocative':
        return 'vocative'
    # appositional modifier
    elif t.dep_label == 'app':
        return 'appos'
    # comparative adverbial clause or comparative oblique nominal
    elif t.dep_label == 'adjunct_compar':
        if (t.upos == 'ADJ' and t.pos == 'ppas' and t.children_with_label('aux') and t.children_with_ud_label('mark') or
            t.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN'] and t.children_with_ud_label('mark') and t.children_with_ud_label('cop') or
            t.upos in ['VERB']):
            return 'advcl:cmpr'
        else:
            return 'obl:cmpr'
    # direct speech
    elif t.dep_label == 'adjunct_qt':
        return 'parataxis:obj'
    # inclusions
    elif t.dep_label == 'adjunct_comment':
        return 'parataxis:insert'
    # relative clause modifier of the matrix clause or relative clause modifier of a noun
    elif t.dep_label == 'adjunct_rc':
        if t.upos == 'VERB':
            return 'advcl:relcl'
        else:
            return 'acl:relcl'
    # possessive nominal modifier or possessive determiner
    elif t.dep_label == 'adjunct_poss':
        if t.upos in ['NOUN', 'PRON', 'PROPN', 'ADJ']:
            return 'nmod:poss'
        elif t.upos == 'DET':
            return 'det:poss'
    # emphatic adverb
    elif t.dep_label == 'adjunct_emph':
        return 'advmod:emph'
    # dependent of an ellided predicate
    elif t.dep_label == 'orphan':
        return 'orphan'
    # marker of relative clause
    elif t.dep_label == 'mark_rel':
        return 'mark_rel'
    # nmod
    elif t.dep_label == 'adjunct_title':
        if t.upos in ['NOUN', 'X']:
            return 'nmod'
    # modifier
    elif t.dep_label.startswith('adjunct_') and t.dep_label not in ['adjunct_compar', 'adjunct_qt', 'adjunct_comment',
                                                                    'adjunct_rc', 'adjunct_poss', 'adjunct_title', 'adjunct_emph']:
        return modifier(t)
    # adjunct
    elif t.dep_label == 'adjunct':
        return modifier(t)
    # clausal complement
    elif t.dep_label == 'comp':
        mark = t.child_with_ud_label('mark')
        if t.gov.upos in ['PROPN', 'NOUN', 'X', 'NUM', 'SYM']:
            if (t.gov.pos.startswith('ger') or
                t.upos == 'VERB' and mark or
                t.upos == 'ADJ' and mark and (t.child_with_label('aux') or t.child_with_ud_label('cop'))):
                return verb_complement(t)
            elif t.upos == 'ADJ' and not mark:
                return 'nmod:arg'
            elif t.gov.upos == 'ADV' and mark:
                return verb_complement(t)
            elif t.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'ADJ', 'DET', 'NUM', 'SYM']:
                if mark:
                    return verb_complement(t)
                else:
                    return 'nmod:arg'
        elif t.gov.upos == 'ADJ':
            if t.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'ADJ', 'DET', 'NUM', 'SYM']:
                if mark:
                    return verb_complement(t)
                else:
                    return 'obl:arg'
            elif t.upos == 'VERB' and mark:
                return verb_complement(t)
        elif (t.gov.upos in ['VERB', 'ADV'] or 
              t.gov.upos == 'PART' and t.gov.lemma in ['tak', 'chyba', 'prawie', 'pewnie', 'zwłaszcza'] or
              t.gov.upos == 'DET' and t.gov.lemma in ['ten', 'taki'] or
              t.gov.upos == 'INTJ'):
            return verb_complement(t)
        elif t.gov.upos == 'PRON':
            if t.gov.lemma == 'to':
                return verb_complement(t, cleft=True)
            else:
                return 'nmod:arg'
    # clausal complement agent
    elif t.dep_label == 'comp_ag':
        return 'obl:agent'
    # flat expressions
    elif t.dep_label == 'ne':
        if t.upos in ['PROPN', 'X']:
            return 'flat'
        elif t.upos == 'ADJ' or t.upos == 'DET' and t.pos == 'adj':
            return 'amod:flat'
        elif t.upos == 'NOUN':
            return 'nmod:flat'
        elif t.upos == 'NUM':
            return 'nummod:flat'
    # foreign
    elif t.dep_label == 'ne_foreign':
        return 'flat:foreign'
    # reflexive clitic with an inherently reflexive verb
    elif t.dep_label == 'refl' and t.lemma in ['się', 'siebie']:
        return 'expl:pv'
    # imperative auxiliary
    elif t.dep_label == 'imp' and t.lemma in ['niech', 'niechaj', 'niechże', 'niechby']:
        return 'aux:imp'
    # object
    elif t.dep_label == 'obj':
        if (t.children_with_ud_label('mark') and (t.upos == 'ADJ' and t.pos == 'ppas' and t.children_with_label('aux') or
            t.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'VERB', 'ADV']) or
            t.upos == 'VERB'):
            return 'ccomp:obj'
        elif (t.upos == 'SYM' and t.form in ['%', '$'] or
            t.upos in ['PROPN', 'NOUN', 'PRON', 'ADJ', 'NUM', 'X', 'DET'] and not t.children_with_ud_label('case') or
            t.upos in ['ADV', 'PART']):
            return 'obj'
    # indirect object
    elif t.dep_label.startswith('obj_'):
        return 'iobj'
    # nominal modifier predicate or open clausal complement predicate
    elif t.dep_label == 'pd' and t.lemma not in ['być', 'bywać']:
        if t.upos == 'NOUN' and t.gov.lemma in ['być', 'bywać'] and t.gov.upos == 'NOUN':
            return 'nmod:pred'
        else:
            return 'xcomp:pred'
    # punctuation
    elif t.dep_label in ['punct', 'abbrev_punct']:
        return 'punct'
    # root
    elif t.dep_label == 'root':
        return 'root'
    # subject
    elif t.dep_label == 'subj':
        if t.gov.upos == 'ADJ' and t.gov.ufeats['Voice'] == 'Pass':
            if (t.children_with_ud_label('mark') and (t.upos == 'VERB' or
                t.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN'] and t.children_with_ud_label('cop'))):
                return 'csubj:pass'
            else:
                return 'nsubj:pass'
        elif (t.children_with_ud_label('mark') and (t.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'VERB', 'ADV']) or
              t.upos == 'VERB' and t.pos != 'inf'):
            return 'csubj'
        elif t.upos in ['PROPN', 'NOUN', 'PRON', 'ADJ', 'NUM', 'X', 'DET'] and not t.children_with_ud_label('case'):
            if t.gov.pos.startswith('ger'):
                return 'obl:agent'
            else:
                return 'nsubj'
        elif t.upos in ['PROPN', 'NOUN', 'PRON', 'NUM', 'DET'] and t.children_with_ud_label('case') or t.upos == 'SYM' and t.form == '%':
            return 'nsubj'
        elif t.upos == 'ADV' or t.upos == 'VERB' and t.pos == 'inf':
            return 'xcomp:subj'
    # clausal complement
    elif t.dep_label == 'comp_fin':
        return 'ccomp'
    # open clausal complement
    elif t.dep_label == 'comp_inf':
        return 'xcomp'
    # compound
    elif t.dep_label == 'cond' and t.lemma == 'by':
        return 'aux:cnd'
    # mobile inflection
    elif t.dep_label == 'aglt' and t.lemma == 'być':
        return 'aux:clitic'
    # negation
    elif t.dep_label in ['neg', 'cneg']:
        return 'advmod:neg'
    # fixed multiword expressions
    elif t.dep_label == 'mwe':
        if (t.gov.upos == 'NUM' or
            t.gov.upos == 'DET' and t.gov.pos == 'num' and t.upos != 'ADV' or
            t.gov.upos == 'NOUN' and t.gov.lemma == 'setka' or
            t.gov.pos in ['dig', 'brev'] and t.pos == 'dig'):
            return 'flat'
        elif t.upos == 'PUNCT':
            return 'punct'
        else:
            return 'fixed'
    # item
    elif t.dep_label == 'item':
        if t.upos == 'PUNCT':
            return 'punct'
        else:
            return 'list'
    # SPEECH CONVERSION
    elif t.pos in ['fill', 'interp'] and t.dep_label == 'discourse':
        return 'discourse'
    elif t.dep_label == 'reparandum':
        return 'reparandum'
    elif t.dep_label == 'parataxis':
        return 'parataxis'
    elif t.dep_label == 'parataxis_restart':
        return 'parataxis:restart'
    elif t.dep_label == 'dep':
        return 'dep'
    else:
        return t.dep_label


def verb_complement(t: Token, cleft: bool = False) -> str:
    """Helper function for converting verb complements' labels."""
    if cleft:
        if t.upos == 'VERB':
            aux = t.child_with_label('aux')
            if t.ufeats.get('VerbForm') == 'Inf' and not aux:
                return 'xcomp:cleft'
            return 'ccomp:cleft'

        elif t.upos == 'ADJ':
            aux = t.child_with_label('aux')
            cop = t.child_with_ud_label('cop')
            if aux or cop:
                return 'ccomp:cleft'

        elif t.upos in ['NOUN', 'PRON', 'PROPN']:
            cop = t.child_with_ud_label('cop')
            if cop:
                if cop.pos == 'inf':
                    return 'xcomp:cleft'
                return 'ccomp:cleft'

            elif t.upos in ['NOUN', 'PROPN']:
                return 'ccomp:cleft'
    else:
        if t.upos == 'VERB' and t.child_with_ud_label('mark'):
            aux = t.child_with_label('aux')
            if t.ufeats.get('VerbForm') == 'Inf' and not aux:
                return 'xcomp'
            return 'ccomp'

        elif t.upos == 'ADJ' and t.child_with_ud_label('mark'):
            return 'ccomp'

        elif t.upos == 'ADV':
            if t.child_with_ud_label('mark'):
                return 'ccomp'
            return 'advmod:arg'

        elif t.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'DET', 'ADV']:
            if t.child_with_ud_label('mark'):
                cop = t.child_with_ud_label('cop')
                if cop:
                    if cop.pos == 'inf':
                        return 'xcomp'
                    return 'ccomp'
                return 'ccomp'
            return 'obl:arg'

        elif t.upos in ['NUM'] and t.child_with_ud_label('case'):
            return 'obl:arg'

        elif t.upos in ['X', 'SYM'] and t.child_with_ud_label('case'):
            return 'obl:arg'

        elif t.upos == 'PART' and t.child_with_label('mwe'):
            return 'obl:arg'

        elif t.upos == 'ADP' and not t.child_with_ud_label('comp'):
            return 'obl:orphan'

        else:
            return t.udep_label


def modifier(t: Token) -> str:
    """Helper function for converting modifier labels."""
    mark = t.child_with_ud_label('mark')

    if t.gov.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'NUM', 'SYM']:

        if t.upos == 'ADJ':
            if t.pos in ['ppas', 'pact']:
                if mark:
                    if mark.lemma == 'jako' and mark.ufeats.get('ConjType'):
                        return 'amod'
                    else:
                        return adverbial(t)
                else:
                    return 'acl'
            elif t.child_with_ud_label('cop'):
                if mark:
                    return adverbial(t)
                else:
                    return 'acl'
            else:
                if mark:
                    if mark.lemma == 'jako' and mark.ufeats.get('ConjType') and t.gov.pos != 'ger' and t.dep_label == 'adjunct_attrib':
                        return 'amod'
                    else:
                        return adverbial(t)
                elif t.child_with_ud_label('case'):
                    return 'nmod'
                else:
                    return 'amod'

        elif t.upos in ['NOUN', 'PRON', 'PROPN']:
            if t.child_with_ud_label('cop'):
                if mark:
                    return adverbial(t)
                else:
                    return 'acl'
            elif t.dep_label.startswith('adjunct_') and t.gov.child_with_ud_label('cop'):
                return adverbial(t)
            else:
                return 'nmod'

        elif t.upos == 'DET' and t.pos == 'num':
            if t.child_with_ud_label('cop') and mark:
                return adverbial(t)
            else:
                return 'nmod'

        elif t.upos == 'DET' and t.pos == 'adj':
            if mark:
                if mark.lemma == 'jako' and mark.ufeats.get('ConjType'):
                    return 'amod'
                else:
                    if t.child_with_ud_label('case'):
                        return 'nmod'
                    else:
                        return 'amod'

        elif t.upos == 'NUM':
            return 'nmod'

        elif t.upos == 'SYM':
            return 'nmod'

        elif t.pos == 'brev' and t.upos != 'CCONJ':
            if t.lemma in ['były', 'dawny', 'elektro', 'habilitowany', 'maksymalny', 'nad poziomem morza', 'parafialny', 'pięcioprocentowy', 'przed naszą erą',
                           'północny', 'starszy', 'stumililitrowy', 'świętej pamięci', 'święty', 'urodzony', 'wschodni', 'wyżej wymieniony', 'zachodni', 'zbudowany']:
                return 'amod'
            elif t.lemma in ['około']:
                t.upos = 'PART'
                return 'advmod:emph'
            else:
                return 'nmod'

        elif t.upos == 'PART' and t.lemma in PARTICLES:
            if not mark:
                return 'advmod:emph'
            else:
                return adverbial(t)












"""
from utils.node import Node as ND
from utils.feats import UFeats
from utils.feats import Feats
import dependency.extract as extract
from re import *

reAdjunct = compile("^adjunct_")
reGer = compile("^ger")

PARTICLES = ['a', 'aby', 'akurat', 'ale', 'ani', u'azaliż', u'aż', 'ba', 'blisko', 'bodaj', u'bodajże', 'byle', u'chociaż', u'choć', u'choćby', u'chociażby', 'chyba', 'coraz', 'czyli', 'dopiero', 'doprawdy', u'dość', u'dosyć', u'gdzieś', u'głównie', 'i', 'jak', 'jakby', 'jakoby', 'jednak', u'jednakowoż', u'jednakże', 'jedynie', u'jeszcze', u'już', u'może', 'nadto', 'najwidoczniej', u'najwyraźniej', u'najwyżej', u'naprawdę', 'nawet', 'niby', 'nie', 'niejako', 'niemal', u'niemalże', u'niespełna', 'niestety', u'niemniej', u'oczywiście', u'około', 'ot', 'oto', u'otóż', 'pewnie', u'podobnież', 'podobno', 'ponad', 'ponadto', u'poniekąd', u'ponoć', 'prawie', 'przecie', u'przecież', u'przeszło', 'przynajmniej', 'raczej', 'raptem', u'również', u'skądinąd', u'szczególnie', 'tak', u'także', 'to', u'toż', u'trochę', 'tylko', u'też', u'tuż', u'widać', u'widocznie', u'więc', u'właśnie', 'wprawdzie', 'wprost', u'wręcz', 'wreszcie', 'wszak', u'wszakże', 'wszelako', 'z', 'za', 'zaledwie', 'zapewne', 'zaraz', 'zarazem', u'zaś', 'zbyt', u'zgoła', 'znacznie', 'znowu', u'znowuż', u'znów', u'zresztą', u'zwłaszcza', u'że', u'szczególnie', 'istotnie', 'praktycznie']

def modifier(dg, e, gov, n):
    ret = e[2]['ud_label']
    if ND().upos(gov) in ['PROPN', 'NOUN', 'PRON', 'X', 'NUM', 'SYM']:
        if ND().upos(n) in ['ADJ']:
            if ND().pos(n) in ['ppas', 'pact']:
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                        ret = 'amod'
                    else:
                        ret = _adverbial(dg, e, gov, n)
                else:
                    ret = 'acl'
            elif extract.dep_via_label(dg, n, 'cop', ud=True):
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    ret = _adverbial(dg, e, gov, n)
                else:
                    ret = 'acl'
            else:
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType') and ND().pos(gov) != 'ger' and e[2]['label'] == 'adjunct_attrib':
                        ret = 'amod'
                    else:
                        ret = _adverbial(dg, e, gov, n)
                elif extract.dep_via_label(dg, n, 'case', ud=True):
                    ret = 'nmod'
                else:
                    ret = 'amod'
        elif ND().upos(n) in ['NOUN', 'PRON', 'PROPN']:
            if extract.dep_via_label(dg, n, 'cop', ud=True):
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    ret = _adverbial(dg, e, gov, n)
                else:
                    ret = 'acl'
            elif reAdjunct.search(e[2]['label']) and extract.dep_via_label(dg, gov, 'cop', ud=True):
                ret = _adverbial(dg, e, gov, n)
            else:
                ret = 'nmod'
        elif ND().upos(n) in ['DET'] and ND().pos(n) in ['num']:
            if extract.dep_via_label(dg, n, 'cop', ud=True) and extract.dep_via_label(dg, n, 'mark', ud=True):
                ret = _adverbial(dg, e, gov, n)
            else:
                ret = 'nmod'
        elif ND().upos(n) in ['DET'] and ND().pos(n) in ['adj']:
            if extract.dep_via_label(dg, n, 'mark', ud=True) and ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                ret = 'amod'
            else:
                if extract.dep_via_label(dg, n, 'case', ud=True):
                    ret = 'nmod'
                else:
                    ret = 'amod'
        elif ND().upos(n) in ['NUM']:
            ret = 'nmod'
        elif ND().upos(n) in ['SYM']:
            ret = 'nmod'
        elif ND().pos(n) == 'brev' and ND().upos(n) not in ['CCONJ']:
            if ND().lemma(n) in [u'były', 'dawny', 'elektro', 'habilitowany', 'maksymalny', u'nad poziomem morza', 'parafialny', u'pięcioprocentowy', u'przed naszą erą', u'północny', 'starszy', 'stumililitrowy', u'świętej pamięci', u'święty', 'urodzony', 'wschodni', u'wyżej wymieniony', 'zachodni', 'zbudowany']:
                ret = 'amod'
            elif ND().lemma(n) in [u'około']:
                dg.nodes[n[0]]['upos'] = 'PART'
                #ND().upos(n) = 'PART'
                ret = 'advmod:emph'
            else:
                ret = 'nmod'
        elif ND().upos(n) == 'PART' and ND().lemma(n) in PARTICLES:
            if extract.dep_via_label(dg, n, 'mark', ud=True) is None:
                if e[2]['label'] in ['adjunct']:
                    ret = 'advmod:emph'
                else:
                    ret = 'advmod:emph'
            else:
                ret = _adverbial(dg, e, gov, n)
        elif ND().upos(n) in ['VERB']:
            if e[2]['label'] == 'adjunct_attrib':
                ret = 'acl'
            else:
                ret = _adverbial(dg, e, gov, n)
        elif ND().upos(n) in ['ADV']:
            if e[2]['label'] == 'adjunct_attrib':
                ret = 'amod'
            else:
                ret = _adverbial(dg, e, gov, n)
        elif ND().upos(n) == 'X' and ND().pos(n) in ['dig', 'romandig', 'ign']:
            ret = 'amod'
        elif ND().upos(n) == 'ADP' and e[2]['label'] == 'adjunct_attrib':
            ret = 'nmod'
        else:
            ret = _adverbial(dg, e, gov, n)
    elif ND().upos(gov) in ['DET'] and ND().pos(gov) in ['num', 'adj']:
        if ND().upos(n) in ['ADJ']:
            if ND().pos(n) in ['ppas', 'pact']:
                ret = 'acl'
            else:
                if extract.dep_via_label(dg, n, 'case', ud=True):
                    ret = 'nmod'
                else:
                    ret = 'amod'
        elif ND().upos(n) in ['NOUN', 'PRON', 'PROPN']:
            ret = 'nmod'
        elif ND().upos(n) in ['DET'] and ND().pos(n) in ['adj']:
            ret = 'nmod'
        elif ND().upos(n) in ['NUM', 'SYM']:
            ret = 'nmod'
        elif ND().pos(n) == 'brev':
            ret = 'nmod'
        elif ND().upos(n) == 'PART' and extract.dep_via_label(dg, n, 'mark', ud=True) is None:
            if ND().lemma(n) in PARTICLES:
                if e[2]['label'] in ['adjunct']:
                    ret = 'advmod:emph'
                else:
                    ret = 'advmod:emph'
            else:
                ret = 'advmod'
        elif ND().upos(n) == 'VERB':
            ret = _adverbial(dg, e, gov, n)
        elif ND().upos(n) == 'ADV':
            if e[2]['label'] == 'adjunct_attrib':
                ret = 'amod'
            else:
                ret = _adverbial(dg, e, gov, n)
        else:
            ret = _adverbial(dg, e, gov, n)
    elif ND().upos(gov) in ['ADJ']:
        if ND().pos(gov) in ['ppas', 'pact']:
            if ND().upos(n) in ['ADJ'] and e[1] < e[0] and \
                    extract.dep_via_label(dg, n, 'case', ud=True) is None and \
                    extract.dep_via_label(dg, n, 'mark', ud=True) is None and \
                    extract.dep_via_label(dg, gov, 'aux') is None:
                ret = 'amod'
            else:
                ret = _adverbial(dg, e, gov, n)
        else:
            if ND().upos(n) in ['ADJ']:
                if ND().pos(n) in ['ppas', 'pact']:
                    if extract.dep_via_label(dg, n, 'mark', ud=True):
                        ret = _adverbial(dg, e, gov, n)
                    else:
                        ret = 'acl'
                else:
                    if extract.dep_via_label(dg, n, 'mark', ud=True):
                        ret = _adverbial(dg, e, gov, n)
                    elif extract.dep_via_label(dg, n, 'case', ud=True):
                        ret = 'nmod'
                    else:
                        ret = 'amod'
            else:
                ret = _adverbial(dg, e, gov, n)
    elif ND().upos(gov) in ['VERB', 'ADV', 'PART', 'INTJ', 'SCONJ']:
        ret = _adverbial(dg, e, gov, n)
    elif ND().upos(gov) == 'ADP' and extract.dep_via_label(dg, n, 'mwe'):
        if ND().upos(n) == 'ADP' and extract.dep_via_label(dg, n, 'mwe'):
            ret = 'advmod'
        elif ND().upos(n) == 'ADV':
            ret = _adverbial(dg, e, gov, n)
        elif ND().upos(n) == 'PART' and ND().lemma(n) in PARTICLES and extract.dep_via_label(dg, n, 'mark', ud=True) is None:
            ret = 'advmod:emph'
        elif ND().upos(n) == 'CCONJ' and extract.dep_via_label(dg, n, 'conjunct') is None:
            ret = 'cc'
    else:
        ret = _adverbial(dg, e, gov, n)
    return ret


def _adverbial(dg, e, gov, n):
    ret = e[2]['ud_label']
    if ND().upos(n) in ['VERB']:
        ret = 'advcl'
    elif ND().upos(n) in ['ADV']:
        if extract.dep_via_label(dg, n, 'mark', ud=True):
            ret = 'advcl'
        else:
            ret = 'advmod'
    elif ND().upos(n) in ['ADP'] and extract.dep_via_label(dg, n, 'mwe'):
        ret = 'advmod'
    elif ND().upos(n) == 'PART':
        if extract.dep_via_label(dg, n, 'mark', ud=True) is None:
            if ND().lemma(n)in PARTICLES:
                if e[2]['label'] in ['adjunct']:
                    ret = 'advmod:emph'
                else:
                    ret = 'advmod:emph'
            else:
                ret = 'advmod'
        else:
            ret = 'advcl'
    elif ND().upos(n) in ['PRON', 'NOUN', 'X', 'PROPN', 'NUM', 'SYM']:
        if extract.dep_via_label(dg, n, 'mark', ud=True):
            if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                ret = 'obl'
            else:
                ret = 'advcl'
        else:
            ret = 'obl'
    elif ND().upos(n) in ['ADJ']:
        if ND().pos(n) in ['ppas', 'pact']:
            if extract.dep_via_label(dg, n, 'mark', ud=True):
                if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                    ret = 'obl'
                else:
                    ret = 'advcl'
            else:
                if extract.dep_via_label(dg, n, 'case', ud=True):
                    ret = 'obl'
                else:
                    ret = 'xcomp'
        else:
            if extract.dep_via_label(dg, n, 'mark', ud=True):
                if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                    ret = 'obl'
                else:
                    ret = 'advcl'
            else:
                ret = 'obl'
    elif ND().upos(n) == 'DET' and ND().pos(n) in ['num', 'adj']:
        if extract.dep_via_label(dg, n, 'mark', ud=True):
            if ND().lemma(extract.dep_via_label(dg, n, 'mark', ud=True)) == 'jako' and UFeats().ufeat(extract.dep_via_label(dg, n, 'mark', ud=True), 'ConjType'):
                ret = 'obl'
            else:
                ret = 'advcl'
        else:
            ret = 'obl'
    elif ND().lemma(n)in ['to', u'dopóty'] and ND().pos(n) in ['comp', 'conj']:
        if len(list(dg.successors(e[1]))) == 0:
            ret = 'mark'
        elif len(list(dg.successors(e[1]))) > 0:
            check = True
            for x in dg.successors(e[1]):
                if dg.nodes[x]['upos'] not in ['PUNCT', 'PART']:
                    check = False
            if check is True:
                ret = 'mark'
    elif ND().upos(n) == 'CCONJ' and extract.dep_via_label(dg, n, 'conjunct') is None:
        ret = 'cc'
    return ret
from utils.node import Node as ND
from utils.feats import UFeats
from utils.feats import Feats
import dependency.extract as extract
from re import *

def complement(dg, e, gov, n):
    ret = e[2]['ud_label']
    if ND().upos(gov) in ['PROPN', 'NOUN', 'X', 'NUM', 'SYM']:
        if ND().pos(gov) == 'ger':
            ret = _verb_complement(dg, e, gov, n)
        else:
            if ND().upos(n) == 'VERB' and extract.dep_via_label(dg, n, 'mark', ud=True):
                ret = _verb_complement(dg, e, gov, n)
            elif ND().upos(n) in ['ADJ']:
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    if extract.dep_via_label(dg, n, 'aux'):
                        ret = _verb_complement(dg, e, gov, n)
                    elif extract.dep_via_label(dg, n, 'cop', ud=True):
                        ret = _verb_complement(dg, e, gov, n)
                else:
                    ret = 'nmod:arg'
            elif ND().upos(n) == 'ADV' and extract.dep_via_label(dg, n, 'mark', ud=True):
                if extract.dep_via_label(dg, n, 'aux'):
                    ret = _verb_complement(dg, e, gov, n)
                else:
                    ret = _verb_complement(dg, e, gov, n)
            elif ND().upos(n) in ['PROPN', 'NOUN', 'PRON', 'X', 'DET', 'NUM']:
                if extract.dep_via_label(dg, n, 'mark', ud=True):
                    if extract.dep_via_label(dg, n, 'aux'):
                        ret = _verb_complement(dg, e, gov, n)
                    elif extract.dep_via_label(dg, n, 'cop', ud=True):
                        ret = _verb_complement(dg, e, gov, n)
                    else:
                        ret = _verb_complement(dg, e, gov, n)
                else:
                    ret = 'nmod:arg'
    elif ND().upos(gov) == 'ADJ':
        if ND().upos(n) in ['PROPN', 'NOUN', 'PRON', 'X', 'ADJ', 'DET', 'NUM', 'SYM']:
            if extract.dep_via_label(dg, n, 'mark', ud=True):
                ret = _verb_complement(dg, e, gov, n)
            else:
                ret = 'obl:arg'
        elif ND().upos(n) in ['VERB'] and extract.dep_via_label(dg, n, 'mark', ud=True):
            ret = _verb_complement(dg, e, gov, n)
    elif ND().upos(gov) in ['VERB', 'ADV']:
        ret = _verb_complement(dg, e, gov, n)
    elif ND().upos(gov) == 'PART' and ND().lemma(gov) in ['tak', 'chyba', 'prawie', 'pewnie', u'zwłaszcza']:
        ret = _verb_complement(dg, e, gov, n)
    elif ND().upos(gov) == 'DET' and ND().lemma(gov) in ['ten', 'taki']:
        ret = _verb_complement(dg, e, gov, n)
    elif ND().upos(gov) == 'PRON':
        if ND().lemma(gov) == 'to':
            ret = _verb_complement(dg, e, gov, n, cleft=True)
        else:
            ret = 'nmod:arg'
    elif ND().upos(gov) == 'INTJ':
        ret = _verb_complement(dg, e, gov, n)
    return ret


def _verb_complement(dg, e, gov, n, cleft=False):
    ret = e[2]['ud_label']
    if cleft is True:
        if ND().upos(n) == 'VERB' and extract.dep_via_label(dg, n, 'mark', ud=True):
            if UFeats().ufeat(n, 'VerbForm') == 'Inf' and extract.dep_via_label(dg, n, 'aux') is None:
                ret = 'xcomp:cleft'
            else:
                ret = 'ccomp:cleft'
        elif ND().upos(n) == 'ADJ' and extract.dep_via_label(dg, n, 'mark', ud=True):
            if extract.dep_via_label(dg, n, 'aux'):
                ret = 'ccomp:cleft'
            elif extract.dep_via_label(dg, n, 'cop', ud=True):
                ret = 'ccomp:cleft'
        elif ND().upos(n) in ['NOUN', 'PRON', 'PROPN'] and extract.dep_via_label(dg, n, 'cop', ud=True) and extract.dep_via_label(dg, n, 'mark', ud=True):
            if ND().pos(extract.dep_via_label(dg, n, 'cop', ud=True)) == 'inf':
                ret = 'xcomp:cleft'
            else:
                ret = 'ccomp:cleft'
        elif ND().upos(n) in ['NOUN', 'PROPN'] and extract.dep_via_label(dg, n, 'cop', ud=True) is None and extract.dep_via_label(dg, n, 'mark', ud=True):
            ret = 'ccomp:cleft'
    else:
        if ND().upos(n) == 'VERB' and extract.dep_via_label(dg, n, 'mark', ud=True):
            if UFeats().ufeat(n, 'VerbForm') == 'Inf' and extract.dep_via_label(dg, n, 'aux') is None:
                ret = 'xcomp'
            else:
                ret = 'ccomp'
        elif ND().upos(n) == 'ADJ' and extract.dep_via_label(dg, n, 'mark', ud=True):
            ret = 'ccomp'
        elif ND().upos(n) == 'ADV':
            if extract.dep_via_label(dg, n, 'mark', ud=True):
                ret = 'ccomp'
            else:
                ret = 'advmod:arg'
        elif ND().upos(n) in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'DET', 'ADV']:
            if extract.dep_via_label(dg, n, 'mark', ud=True):
                if extract.dep_via_label(dg, n, 'cop', ud=True):
                    if ND().pos(extract.dep_via_label(dg, n, 'cop', ud=True)) == 'inf':
                        ret = 'xcomp'
                    else:
                        ret = 'ccomp'
                else:
                    ret = 'ccomp'
            else:
                ret = 'obl:arg'
        elif ND().upos(n) in ['NUM'] and extract.dep_via_label(dg, n, 'case', ud=True):
            ret = 'obl:arg'
        elif ND().upos(n) in ['X', 'SYM'] and extract.dep_via_label(dg, n, 'case', ud=True):
            ret = 'obl:arg'
        elif ND().upos(n) == 'PART' and extract.dep_via_label(dg, n, 'mwe'):
            ret = 'obl:arg'
        elif ND().upos(n) == 'ADP' and extract.dep_via_label(dg, n, 'comp') is None:
            ret = 'obl:orphan'
    return ret
"""