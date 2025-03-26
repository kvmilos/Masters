"""
A dictionary for possible feats based on POS.
"""

feats_of_pos = {
    'subst': ['number', 'case', 'gender', 'subgender'],
    'num': ['number', 'case', 'gender'],
    'numcol': ['number', 'case', 'gender'],
    'adjnum': ['number', 'case', 'gender', 'degree'],
    'advnum': ['degree'],
    'adj': ['number', 'case', 'gender', 'degree'],
    'adja': [],
    'adjb': ['number', 'case', 'gender', 'degree'],
    'adv': ['degree'],
    'ppron12': ['number', 'case', 'gender', 'person', 'accentability'],
    'ppron3': ['number', 'case', 'gender', 'person', 'accentability', "post-prepositionality"],
    'siebie': ['case'],
    'prep': ['case', 'vocalicity'],
    'conj': [],
    'comp': [],
    'part': ['vocalicity'],
    'interj': [],
    'fin': ['number', 'person', 'aspect'],
    'bedzie': ['number', 'person', 'aspect'],
    'praet': ['number', 'gender', 'aspect', 'agglutination'],
    'impt': ['number', 'person', 'aspect'],
    'imps': ['aspect'],
    'inf': ['aspect'],
    'ger': ['number', 'case', 'gender', 'aspect', 'negation'],
    'pcon': ['aspect'],
    'pant': ['aspect'],
    'pact': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'],
    'pactb': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'],
    'ppas': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'],
    'ppasb': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'],
    'ppraet': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'], #degree???
    'fut': ['number', 'person', 'aspect'],
    'plusq': ['number', 'gender', 'aspect', 'vocalicity'], #vocalicity???
    'aglt': ['number', 'person', 'aspect', 'vocalicity'],
    'agltaor': ['number', 'person', 'aspect', 'vocalicity'],
    'winien': ['number', 'gender', 'aspect'],
    'pred': [],
    'brev': ['fullstoppedness'],
    'frag': [],
    'interp': [],
    'xxx': [],
    'dig': [],
    'romandig': [],
    'ignndm': [],
    'ign': [],
    'sym': [], # ???
    'incert': [] # ???
}
