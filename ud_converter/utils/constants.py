"""
Constants for the UD Converter project.

This module collects various constant dictionaries used across the project:

1. feats_dict:
   Maps abbreviated feature strings to their corresponding categories.
   For example, 'sg' → 'number', 'nom' → 'case', etc.

2. FEATS_UPDATE:
   Provides updated (UD) values for token features.
   For example, 'nom' → 'Nom', 'sg' → 'Sing', etc.

3. MULTIWORD_EXPRESSIONS:
   Contains variants of multiword expressions mapped to a normalized form.
   This is used to standardize multiword expressions across the corpus.

4. feats_of_pos:
   Maps POS tags to a list of possible feature categories.
   For example, 'subst' → ['number', 'case', 'gender', 'subgender'].
"""

# Dictionary mapping token feature abbreviations to their corresponding categories.
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
    'm': 'gender',
    'p1': 'gender', # obsługa p1 do usunięcia
    'p2': 'gender', # obsługa p2 do usunięcia
    'manim1': 'gender',
    'manim2': 'gender',
    'pri': 'person',
    'sec': 'person',
    'ter': 'person',
    'pos': 'degree',
    'com': 'degree',
    'sup': 'degree',
    'pt': 'subgender', # obsługa pt do dodania
    'akc': 'accentability',
    'nakc': 'accentability',
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

# Dictionary for updating feature values to UD-compatible ones.
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

# Dictionary for normalizing multiword expressions.
MULTIWORD_EXPRESSIONS = {
    'i_tak_dalej': 'i_tak_dalej',
    'i tak dalej': 'i_tak_dalej',
    'i tak dalej': 'i_tak_dalej',
    'i tym podobne': 'i_tym_podobne',
    'i_tym_podobne': 'i_tym_podobne',
    'i tym podobne': 'i_tym_podobne',
    'to_jest': 'to_jest',
    'to jest': 'to_jest',
    'to jest': 'to_jest',
    'na_przykład': 'na_przykład',
    'na przykład': 'na_przykład',
    'na przykład': 'na_przykład',
    'tak_zwany': 'tak_zwany',
    'tak zwany': 'tak_zwany',
    'tak zwany': 'tak_zwany',
    'między innymi': 'między_innymi',
    'między_innymi': 'między_innymi',
    'między innymi': 'między_innymi',
    'bieżącego_rok': 'bieżący_rok',
    'bieżącego rok': 'bieżący_rok',
    'bieżącego rok': 'bieżący_rok',
    'bieżący_rok': 'bieżący_rok',
    'bieżący rok': 'bieżący_rok',
    'bieżący rok': 'bieżący_rok',
    'do_spraw': 'do_spraw',
    'do spraw': 'do_spraw',
    'do spraw': 'do_spraw',
    'w_sprawie': 'w_sprawie',
    'w sprawie': 'w_sprawie',
    'w sprawie': 'w_sprawie',
    'na_temat': 'na_temat',
    'na temat': 'na_temat',
    'na temat': 'na_temat',
    'pod tytułem': 'pod_tytułem',
    'pod_tytułem': 'pod_tytułem',
    'pod tytułem': 'pod_tytułem',
    'bieżący_miesiąc': 'bieżący_miesiąc',
    'bieżący miesiąc': 'bieżący_miesiąc',
    'bieżący miesiąc': 'bieżący_miesiąc',
    'post_scriptum': 'post_scriptum',
    'post scriptum': 'post_scriptum',
    'post scriptum': 'post_scriptum',
    'to_znaczy': 'to_znaczy',
    'to znaczy': 'to_znaczy',
    'to znaczy': 'to_znaczy',
    'pod_nazwą': 'pod_nazwą',
    'pod nazwą': 'pod_nazwą',
    'pod nazwą': 'pod_nazwą',
    'ubiegły_rok': 'ubiegły_rok',
    'ubiegły rok': 'ubiegły_rok',
    'ubiegły rok': 'ubiegły_rok',
    'spółka akcyjna': 'spółka_akcyjna',
    'spółka_akcyjna': 'spółka_akcyjna',
    'spółka akcyjna': 'spółka_akcyjna',
    'świętej_pamięci': 'świętej_pamięci',
    'świętej pamięci': 'świętej_pamięci',
    'świętej pamięci': 'świętej_pamięci',
    'kilometr_kwadratowy': 'kilometr_kwadratowy',
    'kilometr kwadratowy': 'kilometr_kwadratowy',
    'kilometr kwadratowy': 'kilometr_kwadratowy',
    'pod_wezwaniem': 'pod_wezwaniem',
    'pod wezwaniem': 'pod_wezwaniem',
    'pod wezwaniem': 'pod_wezwaniem',
    'nad_poziomem_morza': 'nad_poziomem_morza',
    'nad poziomem morza': 'nad_poziomem_morza',
    'nad poziomem morza': 'nad_poziomem_morza',
    'ograniczona_odpowiedzialność': 'ograniczona_odpowiedzialność',
    'ograniczona odpowiedzialność': 'ograniczona_odpowiedzialność',
    'ograniczona odpowiedzialność': 'ograniczona_odpowiedzialność',
    'Immunoglobina_E': 'Immunoglobina_E',
    'Immunoglobina E': 'Immunoglobina_E',
    'Immunoglobina E': 'Immunoglobina_E',
    'wyżej_wymieniony': 'wyżej_wymieniony',
    'wyżej wymieniony': 'wyżej_wymieniony',
    'wyżej wymieniony': 'wyżej_wymieniony',
    'przed_naszą_erą': 'przed_naszą_erą',
    'przed naszą_erą': 'przed_naszą_erą',
    'przed naszą_erą': 'przed_naszą_erą'
}

# Dictionary for possible features based on POS.
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
    'ppraet': ['number', 'case', 'gender', 'degree', 'aspect', 'negation'], # obsługa degree w ppraet do dodania
    'fut': ['number', 'person', 'aspect'],
    'plusq': ['number', 'gender', 'aspect'],
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
    'sym': [],
    'incert': []
}

# List of particles
PARTICLES = ['a', 'aby', 'akurat', 'ale', 'ani', 'azaliż', 'aż', 'ba', 'blisko', 'bodaj', 'bodajże', 'byle', 'chociaż', 'choć',
            'choćby', 'chociażby', 'chyba', 'coraz', 'czyli', 'dopiero', 'doprawdy', 'dość', 'dosyć', 'gdzieś', 'głównie', 'i',
            'jak', 'jakby', 'jakoby', 'jednak', 'jednakowoż', 'jednakże', 'jedynie', 'jeszcze', 'już', 'może', 'nadto', 'najwidoczniej',
            'najwyraźniej', 'najwyżej', 'naprawdę', 'nawet', 'niby', 'nie', 'niejako', 'niemal', 'niemalże', 'niespełna', 'niestety',
            'niemniej', 'oczywiście', 'około', 'ot', 'oto', 'otóż', 'pewnie', 'podobnież', 'podobno', 'ponad', 'ponadto',
            'poniekąd', 'ponoć', 'prawie', 'przecie', 'przecież', 'przeszło', 'przynajmniej', 'raczej', 'raptem', 'również',
            'skądinąd', 'szczególnie', 'tak', 'także', 'to', 'toż', 'trochę', 'tylko', 'też', 'tuż', 'widać', 'widocznie',
            'więc', 'właśnie', 'wprawdzie', 'wprost', 'wręcz', 'wreszcie', 'wszak', 'wszakże', 'wszelako', 'z', 'za', 'zaledwie',
            'zapewne', 'zaraz', 'zarazem', 'zaś', 'zbyt', 'zgoła', 'znacznie', 'znowu', 'znowuż', 'znów', 'zresztą', 'zwłaszcza',
            'że', 'szczególnie', 'istotnie', 'praktycznie']
