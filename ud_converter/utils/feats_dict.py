"""
Dictionary of possible feats for a token, mapped to their categories.
"""

feats_dict = {
    'sg': 'number',
    'pl': 'number',
    'du': 'number',
    'nom': 'case',
    'acc': 'case',
    'gen': 'case',
    'dat': 'case',
    'loc': 'case',
    'inst': 'case',
    'voc': 'case',
    'f': 'gender',
    'n': 'gender',
    'n2': 'gender',
    'm': 'gender',
    'p1': 'gender',
    'p2': 'gender',
    'manim1': 'gender',
    'manim2': 'gender',
    'pri': 'person',
    'sec': 'person',
    'ter': 'person',
    'pos': 'degree',
    'com': 'degree',
    'sup': 'degree',
    'pt': 'subgender',
    'akc': 'accentability',
    'nakc': 'accentability',
    'zneut': 'accentability',
    'neut': 'accentability',
    'praep': 'post-prepositionality',
    'npraep': 'post-prepositionality',
    'wok': 'vocalicity',
    'nwok': 'vocalicity',
    'perf': 'aspect',
    'imperf': 'aspect',
    'biasp': 'aspect',
    'agl': 'agglutination',
    'nagl': 'agglutination',
    'aff': 'negation',
    'neg': 'negation',
    'pun': 'fullstoppedness',
    'npun': 'fullstoppedness'
}

FEATS_UPDATE = {
    'nom': 'Nom', 'gen': 'Gen', 'dat': 'Dat', 'acc': 'Acc', 'loc': 'Loc', 'inst': 'Ins', 'voc': 'Voc',
    'sg': 'Sing', 'pl': 'Plur', 'du': 'Dual',
    'pos': 'Pos', 'com': 'Cmp', 'sup': 'Sup',
    'perf': 'Perf', 'imperf': 'Imp', 'biasp': 'XXX',
    'pri': '1', 'sec': '2', 'ter': '3',
    'aff': 'Pos', 'neg': 'Neg',
    'praep': 'Pre', 'npraep': 'Npr',
    'akc': 'Long', 'nakc': 'Short'
}
