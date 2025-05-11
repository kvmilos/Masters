"""
Module for dependency label conversion from MPDT to Universal Dependencies format.

This module implements the mapping of dependency labels from the Middle Polish
Dependency Treebank format to Universal Dependencies format, considering the
specific syntactic context of each token to determine the appropriate UD label.
"""
import logging
from utils.classes import Sentence, Token
from utils.constants import PARTICLES
from utils.logger import ChangeCollector
logger = logging.getLogger('ud_converter.dependency.labels')


def labels_conversion(s: Sentence) -> None:
    """
    Converts dependency labels from MPDT to UD format.

    This function iterates over all tokens in the sentence and applies the
    label conversion function to each token.

    :param Sentence s: The sentence to convert
    """
    for t in s.tokens:
        t.udep_label = convert_label(t)


def convert_label(t: Token, gov: Token | None = None, n: Token | None = None, relation_gov: Token | None = None) -> str:
    """
    Converts a dependency label from MPDT format to Universal Dependencies format.

    This function applies a series of rules to determine the appropriate UD
    dependency label based on the token's part of speech, lemma, syntactic context,
    and original dependency label in the MPDT format.

    :param Token t: The token for which to convert the dependency label
    :param Token gov: An optional token for additional context (governor)
    :param Token n: An optional token for additional context (current token)
    :return: The converted Universal Dependencies dependency label
    :rtype: str
    """
    n = n or t
    gov = gov or t.gov
    relation_gov = relation_gov or t.gov2

    if relation_gov == t.ugov and t.udep_label != '_':
        return t.udep_label

    # discourse element (emoji)
    if t.pos == 'sym' and t.dep_label == 'adjunct_comment':
        return 'discourse'
    # discourse element (interjection)
    elif t.pos == 'interj' and t.dep_label != 'root':
        return 'discourse:intj'
    # subordinating conjunction
    elif t.lemma == 'o' and len(t.children_with_lemma('tyle')) == 1 and t.children_with_lemma('tyle')[0].dep_label == 'mwe':
        return 'mark'
    elif t.lemma == 'o' and len(t.children_with_lemma('tyle')) > 1:
        ChangeCollector.record(t.sentence.id, t.id, "Multiple 'tyle'-lemma children for o", module="labels", level="WARNING")
    # possessive determiner or determiner
    elif n.upos == 'DET' and t.pos != 'num' and t.dep_label in ['adjunct', 'poss']:
        if t.ufeats.get('Poss') == 'Yes':
            return 'det:poss'
        else:
            return 'det'
    # passive auxiliary or auxiliary
    elif t.dep_label == 'aux':
        if t.gov2 and t.gov2.pos == 'ppas':
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
        if (
            n.upos == 'ADJ' and t.pos == 'ppas' and t.children_with_label('aux') and t.children_with_ud_label('mark')
            or n.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN'] and t.children_with_ud_label('mark') and t.children_with_ud_label('cop')
            or n.upos in ['VERB']
        ):
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
        if n.upos == 'VERB':
            return 'advcl:relcl'
        else:
            return 'acl:relcl'
    # possessive nominal modifier or possessive determiner
    elif t.dep_label == 'adjunct_poss':
        if n.upos in ['NOUN', 'PRON', 'PROPN', 'ADJ']:
            return 'nmod:poss'
        elif n.upos == 'DET':
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
        if n.upos in ['NOUN', 'X']:
            return 'nmod'
    # modifier
    elif t.dep_label.startswith('adjunct_') and t.dep_label not in ['adjunct_compar', 'adjunct_qt', 'adjunct_comment',
                                                                    'adjunct_rc', 'adjunct_poss', 'adjunct_title', 'adjunct_emph']:
        return modifier(t, n)
    # adjunct
    elif t.dep_label == 'adjunct':
        return modifier(t, n)
    # clausal complement
    elif t.dep_label == 'comp':
        mark = t.children_with_ud_label('mark')
        if gov and gov.upos in ['PROPN', 'NOUN', 'X', 'NUM', 'SYM']:
            if (
                gov.pos.startswith('ger')
                or n.upos == 'VERB' and mark
                or n.upos == 'ADJ' and mark and (t.children_with_label('aux') or t.children_with_ud_label('cop'))
            ):
                return verb_complement(t, n)
            elif n.upos == 'ADJ' and not mark:
                return 'nmod:arg'
            elif gov.upos == 'ADV' and mark:
                return verb_complement(t, n)
            elif n.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'ADJ', 'DET', 'NUM', 'SYM']:
                if mark:
                    return verb_complement(t, n)
                else:
                    return 'nmod:arg'
        elif gov and gov.upos == 'ADJ':
            if n.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'ADJ', 'DET', 'NUM', 'SYM']:
                if mark:
                    return verb_complement(t, n)
                else:
                    return 'obl:arg'
            elif n.upos == 'VERB' and mark:
                return verb_complement(t, n)
        elif gov and (gov.upos in ['VERB', 'ADV']
                        or gov.upos == 'PART' and gov.lemma in ['tak', 'chyba', 'prawie', 'pewnie', 'zwłaszcza']
                        or gov.upos == 'DET' and gov.lemma in ['ten', 'taki']
                        or gov.upos == 'INTJ'):
            return verb_complement(t, n)
        elif gov and gov.upos == 'PRON':
            if gov.lemma == 'to':
                return verb_complement(t, n, cleft=True)
            else:
                return 'nmod:arg'
    # clausal complement agent
    elif t.dep_label == 'comp_ag':
        return 'obl:agent'
    # flat expressions
    elif t.dep_label == 'ne':
        if n.upos in ['PROPN', 'X']:
            return 'flat'
        elif n.upos == 'ADJ' or n.upos == 'DET' and t.pos == 'adj':
            return 'amod:flat'
        elif n.upos == 'NOUN':
            return 'nmod:flat'
        elif n.upos == 'NUM':
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
        if (
            t.children_with_ud_label('mark')
            and (
                n.upos == 'ADJ' and t.pos == 'ppas' and t.children_with_label('aux')
                or n.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'VERB', 'ADV']
            )
            or n.upos == 'VERB'
        ):
            return 'ccomp:obj'
        elif (
            n.upos == 'SYM' and t.form in ['%', '$']
            or n.upos in ['PROPN', 'NOUN', 'PRON', 'ADJ', 'NUM', 'X', 'DET'] and not t.children_with_ud_label('case')
            or n.upos in ['ADV', 'PART']
        ):
            return 'obj'
    # indirect object
    elif t.dep_label.startswith('obj_'):
        return 'iobj'
    # nominal modifier predicate or open clausal complement predicate
    elif t.dep_label == 'pd' and t.lemma not in ['być', 'bywać']:
        if n.upos == 'NOUN' and t.gov2 and t.gov2.lemma in ['być', 'bywać'] and t.gov2.upos == 'NOUN':
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
        if t.gov2 and t.gov2.upos == 'ADJ' and t.gov2.ufeats.get('Voice') == 'Pass':
            if (
                t.children_with_ud_label('mark')
                and (
                    n.upos == 'VERB'
                    or n.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN'] and t.children_with_ud_label('cop')
                )
            ):
                return 'csubj:pass'
            else:
                return 'nsubj:pass'
        elif (
            t.children_with_ud_label('mark') and (n.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'VERB', 'ADV'])
            or n.upos == 'VERB' and t.pos != 'inf'
        ):
            return 'csubj'
        elif n.upos in ['PROPN', 'NOUN', 'PRON', 'ADJ', 'NUM', 'X', 'DET'] and not t.children_with_ud_label('case'):
            if t.gov2 and t.gov2.pos.startswith('ger'):
                return 'obl:agent'
            else:
                return 'nsubj'
        elif n.upos in ['PROPN', 'NOUN', 'PRON', 'NUM', 'DET'] and t.children_with_ud_label('case') or n.upos == 'SYM' and t.form == '%':
            return 'nsubj'
        elif n.upos == 'ADV' or n.upos == 'VERB' and t.pos == 'inf':
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
        if t.gov2 and (
            t.gov2.upos == 'NUM'
            or t.gov2.upos == 'DET' and t.gov2.pos == 'num' and n.upos != 'ADV'
            or t.gov2.upos == 'NOUN' and t.gov2.lemma == 'setka'
            or t.gov2.pos in ['dig', 'brev'] and t.pos == 'dig'
        ):
            return 'flat'
        elif n.upos == 'PUNCT':
            return 'punct'
        else:
            return 'fixed'
    # item
    elif t.dep_label == 'item':
        if n.upos == 'PUNCT':
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
    return t.udep_label


def verb_complement(t: Token, n: Token, cleft: bool = False) -> str:
    """
    Helper function for converting verb complement dependencies to UD labels.

    This function determines the correct Universal Dependencies label for verb
    complements based on their syntactic context, including handling cleft
    constructions, infinitives, and various types of clauses.

    :param Token t: The token for which to determine the UD dependency label
    :param Token n: The third token in the construction, if applicable
    :param bool cleft: Boolean flag indicating whether the token is part of a cleft construction
    :return: The appropriate Universal Dependencies dependency label
    :rtype: str
    """
    if cleft:
        if n.upos == 'VERB':
            aux = t.children_with_label('aux')
            if t.ufeats.get('VerbForm') == 'Inf' and not aux:
                return 'xcomp:cleft'
            return 'ccomp:cleft'

        elif n.upos == 'ADJ':
            aux = t.children_with_label('aux')
            cop = t.children_with_ud_label('cop')
            if aux or cop:
                return 'ccomp:cleft'

        elif n.upos in ['NOUN', 'PRON', 'PROPN']:
            cop = t.children_with_ud_label('cop')
            if cop:
                if len(cop) > 1:
                    ChangeCollector.record(t.sentence.id, t.id, f"Multiple copula children for '{t.form}': {[c.form for c in cop]}", module="labels", level="WARNING")
                cop_t = cop[0]
                if cop_t.pos == 'inf':
                    return 'xcomp:cleft'
                return 'ccomp:cleft'

            elif n.upos in ['NOUN', 'PROPN']:
                return 'ccomp:cleft'
    else:
        if n.upos == 'VERB' and t.children_with_ud_label('mark'):
            aux = t.children_with_label('aux')
            if t.ufeats.get('VerbForm') == 'Inf' and not aux:
                return 'xcomp'
            return 'ccomp'

        elif n.upos == 'ADJ' and t.children_with_ud_label('mark'):
            return 'ccomp'

        elif n.upos == 'ADV':
            if t.children_with_ud_label('mark'):
                return 'ccomp'
            return 'advmod:arg'

        elif n.upos in ['ADJ', 'NOUN', 'PRON', 'PROPN', 'DET', 'ADV']:
            if t.children_with_ud_label('mark'):
                cop = t.children_with_ud_label('cop')
                if cop:
                    if len(cop) > 1:
                        ChangeCollector.record(t.sentence.id, t.id, f"Multiple copula children for '{t.form}': {[c.form for c in cop]}", module="labels", level="WARNING")
                    cop_t = cop[0]
                    if cop_t.pos == 'inf':
                        return 'xcomp'
                    return 'ccomp'
                return 'ccomp'
            return 'obl:arg'

        elif n.upos in ['NUM'] and t.children_with_ud_label('case'):
            return 'obl:arg'

        elif n.upos in ['X', 'SYM'] and t.children_with_ud_label('case'):
            return 'obl:arg'

        elif n.upos == 'PART' and t.children_with_label('mwe'):
            return 'obl:arg'

        elif n.upos == 'ADP' and not t.children_with_ud_label('comp'):
            return 'obl:orphan'

    return t.udep_label


def modifier(t: Token, n: Token) -> str:
    """
    Helper function for converting modifier dependencies to UD labels.

    This function determines the appropriate Universal Dependencies label for
    modifiers based on their part of speech, the part of speech of their governor,
    and other syntactic properties. It handles various types of adjectival,
    nominal, and adverbial modifiers.

    :param Token t: The token for which to determine the UD dependency label
    :return: The appropriate Universal Dependencies dependency label
    :rtype: str
    """
    mark = t.children_with_ud_label('mark')
    case = t.children_with_ud_label('case')

    if t.gov2 and t.gov2.upos in ['PROPN', 'NOUN', 'PRON', 'X', 'NUM', 'SYM']:

        if n.upos == 'ADJ':
            if t.pos in ['ppas', 'pact']:
                if mark:
                    if len(mark) > 1:
                        ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
                    mark_t = mark[0]
                    if mark_t.lemma == 'jako' and mark_t.ufeats.get('ConjType'):
                        return 'amod'
                    else:
                        return adverbial(t, n)
                else:
                    return 'acl'
            elif t.children_with_ud_label('cop'):
                if mark:
                    return adverbial(t, n)
                else:
                    return 'acl'
            else:
                if mark:
                    if len(mark) > 1:
                        ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
                    mark_t = mark[0]
                    if mark_t.lemma == 'jako' and mark_t.ufeats.get('ConjType') and t.gov2.pos != 'ger' and t.dep_label == 'adjunct_attrib':
                        return 'amod'
                    else:
                        return adverbial(t, n)
                elif case:
                    return 'nmod'
                else:
                    return 'amod'

        elif n.upos in ['NOUN', 'PRON', 'PROPN']:
            if t.children_with_ud_label('cop'):
                if mark:
                    return adverbial(t, n)
                else:
                    return 'acl'
            elif t.dep_label.startswith('adjunct_') and t.gov2 and t.gov2.children_with_ud_label('cop'):
                return adverbial(t, n)
            else:
                return 'nmod'

        elif n.upos == 'DET' and t.pos == 'num':
            if t.children_with_ud_label('cop') and mark:
                return adverbial(t, n)
            else:
                return 'nmod'

        elif n.upos == 'DET' and t.pos == 'adj':
            if mark:
                if len(mark) > 1:
                    ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
                mark_t = mark[0]
                if mark_t.lemma == 'jako' and mark_t.ufeats.get('ConjType'):
                    return 'amod'
                else:
                    if case:
                        return 'nmod'
                    else:
                        return 'amod'

        elif n.upos == 'NUM':
            return 'nmod'

        elif n.upos == 'SYM':
            return 'nmod'

        elif t.pos == 'brev' and n.upos != 'CCONJ':
            if t.lemma in ['były', 'dawny', 'elektro', 'habilitowany', 'maksymalny', 'nad poziomem morza', 'parafialny', 'pięcioprocentowy', 'przed naszą erą',
                           'północny', 'starszy', 'stumililitrowy', 'świętej pamięci', 'święty', 'urodzony', 'wschodni', 'wyżej wymieniony', 'zachodni', 'zbudowany']:
                return 'amod'
            elif t.lemma in ['około']:
                n.upos = 'PART'
                return 'advmod:emph'
            else:
                return 'nmod'

        elif n.upos == 'PART' and t.lemma in PARTICLES:
            if not mark:
                return 'advmod:emph'
            else:
                return adverbial(t, n)

        elif n.upos == 'VERB':
            if t.dep_label == 'adjunct_attrib':
                return 'acl'
            else:
                return adverbial(t, n)

        elif n.upos == 'ADV':
            if t.dep_label == 'adjunct_attrib':
                return 'amod'
            else:
                return adverbial(t, n)

        elif n.upos == 'X' and t.pos in ['dig', 'romandig', 'ign']:
            return 'amod'

        elif n.upos == 'ADP' and t.dep_label == 'adjunct_attrib':
            return 'nmod'

        return adverbial(t, n)

    elif t.gov2 and t.gov2.upos == 'DET' and t.gov2.pos in ['num', 'adj']:

        if n.upos == 'ADJ':
            if t.pos in ['ppas', 'pact']:
                return 'acl'
            else:
                if case:
                    return 'nmod'
                else:
                    return 'amod'

        elif n.upos in ['NOUN', 'PRON', 'PROPN', 'NUM', 'SYM'] or n.upos == 'DET' and t.pos == 'adj' or t.pos == 'brev':
            return 'nmod'

        elif n.upos == 'PART' and not mark:
            if t.lemma in PARTICLES:
                return 'advmod:emph'
            else:
                return 'advmod'

        elif n.upos == 'VERB':
            return adverbial(t, n)

        elif n.upos == 'ADV':
            if t.dep_label == 'adjunct_attrib':
                return 'amod'
            else:
                return adverbial(t, n)

        else:
            return adverbial(t, n)

    elif t.gov2 and t.gov2.upos == 'ADJ':

        if t.gov2 and t.gov2.pos in ['ppas', 'pact']:
            if n.upos == 'ADJ' and int(t.id) < int(t.gov2.id) and not case and not mark and not t.gov2.children_with_label('aux'):
                return 'amod'
            else:
                return adverbial(t, n)

        else:
            if n.upos == 'ADJ':
                if t.pos in ['ppas', 'pact']:
                    if mark:
                        return adverbial(t, n)
                    else:
                        return 'acl'
                else:
                    if mark:
                        return adverbial(t, n)
                    elif case:
                        return 'nmod'
                    else:
                        return 'amod'
            else:
                return adverbial(t, n)

    elif t.gov2 and t.gov2.upos in ['VERB', 'ADV', 'PART', 'INTJ', 'SCONJ']:
        return adverbial(t, n)

    elif t.gov2 and t.gov2.upos == 'ADP' and t.children_with_label('mwe'):
        if n.upos == 'ADP':
            return 'advmod'
        elif n.upos == 'ADV':
            return adverbial(t, n)
        elif n.upos == 'PART' and t.lemma in PARTICLES and not mark:
            return 'advmod:emph'
        elif n.upos == 'CCONJ' and not t.gov2.children_with_label('conjunct'):
            return 'cc'

    return adverbial(t, n)


def adverbial(t: Token, n: Token) -> str:
    """
    Helper function for converting adverbial dependencies to UD labels.

    This function determines the correct Universal Dependencies label for
    adverbial modifiers, distinguishing between adverbial clauses and simple
    adverbial modifiers based on syntactic context.

    :param Token t: The token for which to determine the UD dependency label
    :param Token n: The third token in the construction, if applicable
    :return: The appropriate Universal Dependencies dependency label
    :rtype: str
    """
    mark = t.children_with_ud_label('mark')

    if n.upos == 'VERB':
        return 'advcl'

    elif n.upos == 'ADV':
        if mark:
            return 'advcl'
        else:
            return 'advmod'

    elif n.upos == 'ADP' and t.children_with_label('mwe'):
        return 'advmod'

    elif n.upos == 'PART':
        if not mark:
            if t.lemma in PARTICLES:
                return 'advmod:emph'
            else:
                return 'advmod'
        else:
            return 'advcl'

    elif n.upos in ['PRON', 'NOUN', 'X', 'PROPN', 'NUM', 'SYM']:
        if mark:
            if len(mark) > 1:
                ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
            if mark[0].lemma == 'jako' and 'ConjType' in mark[0].ufeats:
                return 'obl'
            else:
                return 'advcl'
        else:
            return 'obl'

    elif n.upos == 'ADJ':
        if t.pos in ['ppas', 'pact']:
            if mark:
                if len(mark) > 1:
                    ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
                if mark[0].lemma == 'jako' and 'ConjType' in mark[0].ufeats:
                    return 'obl'
                else:
                    return 'advcl'
            else:
                if t.children_with_ud_label('case'):
                    return 'obl'
                else:
                    return 'xcomp'
        else:
            if mark:
                if len(mark) > 1:
                    ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
                if mark[0].lemma == 'jako' and 'ConjType' in mark[0].ufeats:
                    return 'obl'
                else:
                    return 'advcl'
            else:
                return 'obl'

    elif n.upos == 'DET' and t.pos in ['num', 'adj']:
        if mark:
            if len(mark) > 1:
                ChangeCollector.record(t.sentence.id, t.id, f"Multiple 'mark'-children for '{t.form}': {[m.form for m in mark]}", module="labels", level="WARNING")
            if mark[0].lemma == 'jako' and 'ConjType' in mark[0].ufeats:
                return 'obl'
            else:
                return 'advcl'
        else:
            return 'obl'

    elif t.lemma in ['to', 'dopóty'] and t.pos in ['comp', 'conj']:
        if len(t.children) == 0:
            return 'mark'
        elif len(t.children) > 0:
            if all(child.upos in ['PUNCT', 'PART'] for child in t.children):
                return 'mark'

    elif n.upos == 'CCONJ' and not t.children_with_label('conjunct'):
        return 'cc'

    return t.udep_label
