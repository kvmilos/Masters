"""
Module for other POS-specific conversion, including:
- conjunctions
- interjections
- particles
- prepositions
- abbreviations
- frags
- punctuation
- unknown
- symbols
and other.
"""
from utils.classes import Token
from utils.constants import FEATS_UPDATE as FU


def conj(t: Token) -> None:
    """Converts a conj."""
    t.upos = 'CCONJ'


def comp(t: Token) -> None:
    """Converts a comp."""
    t.upos = 'SCONJ'


def interj(t: Token) -> None:
    """Converts an interj."""
    t.upos = 'INTJ'


def part(t: Token) -> None:
    """Converts a part."""
    if not t.upos:
        if t.lemma == 'się':
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Prs', 'Reflex': 'Yes'}
        elif t.lemma == 'by':
            t.upos = 'AUX'
        elif t.lemma in ['niech', 'niechaj', 'niechże', 'niechby']:
            t.upos = 'AUX'
        elif t.lemma == 'nie':
            t.upos = 'PART'
            t.ufeats = {'Polarity': 'Neg'}
        elif t.lemma in ['czy', 'czyżby', 'azaliż']:
            t.upos = 'PART'
            t.ufeats = {'PartType': 'Int'}
        elif t.lemma in ['czyż', 'czyżby']:
            t.upos = 'PART'
            t.ufeats = {'PartType': 'Int'}
        elif t.lemma == 'może':
            t.upos = 'PART'
            t.ufeats = {'PartType': 'Mod'}
        elif t.lemma == 'co':
            t.upos = 'PRON'
            t.ufeats = {'PronType': 'Rel'}
        else:
            t.upos = 'PART'


def prep(t: Token) -> None:
    """Converts a prep."""
    t.upos = 'ADP'
    t.ufeats = {'AdpType': 'Prep'}
    t.umisc['Case'] = FU[t.feats['case']]
    if 'vocalicity' in t.feats:
        if t.feats['vocalicity'] == 'wok':
            t.ufeats = {'Variant': 'Long'}
        else:
            t.ufeats = {'Variant': 'Short'}


def brev(t: Token) -> None:
    """Converts a brev."""
    t.ufeats = {'Abbr': 'Yes'}
    if t.lemma in ['rok', 'stopień_Celsjusza', 'stopień_Fahrenheita', 'milimetr', 'milimetr_kwadratowy',
                   'milimetr_sześcienny', 'centymetr', 'centymetr_kwadratowy', 'centymetr_sześcienny',
                   'cubic_centimetre', 'decymetr', 'decymetr_kwadratowy', 'decymetr_sześcienny', 'metr',
                   'metr_kwadratowy', 'metr_sześcienny', 'kilometr', 'kilometr_kwadratowy', 'kilometr_sześcienny',
                   'mikrometr', 'hektar', 'dekagram', 'gram', 'miligram', 'mikrogram', 'kilogram', 'megagram',
                   'Celsjusz', 'Celsjusza', 'bilion', 'miliard', 'mililitr', 'milimetr', 'milion', 'gigadżul',
                   'gigaherc', 'kiloherc', 'megaherc', 'kilobajt', 'kilobajt_na_sekundę', 'gigabajt', 'megabajt',
                   'megabajt_na_sekundę', 'kilobit', 'milimol', 'megawat', 'kilowolt', 'kwintal', 'litr', 'mach',
                   'gaus', 'nanometr', 'tesla', 'tona', 'tysiąc',
                   'euro', 'jen', 'funt', 'dolar', 'złoty', 'nowy_polski_złoty', 'jen_japoński',
                   'dolar_amerykański', 'frank_belgijski', 'korona_duńska', 'United_States_Dollar', 'strona',
                   'aleja', 'aluminium', 'architekt', 'archiwum', 'artykuł', 'artysta', 'aspirant',
                   'bieżący_miesiąc', 'bieżący_rok', 'brygada', 'centralne_ogrzewanie', 'ciąg_dalszy',
                   'ciąg_dalszy_nastąpi', 'cytat', 'cześć', 'departament', 'doba', 'docent', 'doktor', 'dolina',
                   'druh', 'dupa', 'dyrekcja', 'dyrektor', 'dywizja', 'dziennik', 'dzień', 'długość', 'editor',
                   'ekwiwalent_wodny', 'era', 'fotograf', 'fotografia', 'fundacja', 'generał', 'gmina', 'godzina',
                   'kilowatogodzina', 'grosz', 'głębokość', 'harcmistrz', 'hel', 'homoseksualista', 'hrabia',
                   'ilustracja', 'imienia', 'informacja', 'inspektor', 'inteligencja', 'inżynier',
                   'jednostka_miary', 'jezioro', 'junior', 'język', 'kapitan', 'kardynał', 'karta', 'kartka',
                   'kategoria', 'klasa', 'kleryk', 'kodeks', 'kodeks_postępowania_cywilnego',
                   'kodeks_prawa_cywilnego', 'kodeks_wykroczeń', 'kolega', 'komandor', 'komendant', 'komisarz',
                   'konstytucja', 'kopalnia', 'koło', 'koń_mechaniczny', 'kościół', 'kościół_katolicki', 'ksiądz',
                   'książę', 'lata', 'lekarz', 'liceum', 'liczba', 'litera', 'magister', 'mecenas', 'medycyna',
                   'miara', 'miasto', 'miasto_stołeczne', 'miesiąc', 'miesięcy', 'mieszkanie', 'mieszkaniec',
                   'miligramorównoważnik', 'milijednostka', 'minimum', 'minister', 'ministerstwo', 'minuta',
                   'nadkomisarz', 'nadinspektor', 'nasza_era', 'naszej_ery', 'numer', 'objętość', 'obwód',
                   'oddział', 'odległość', 'odpowiedzialność', 'ograniczona_odpowiedzialność', 'ojciec',
                   'ojcowie', 'okolica', 'opatrzność', 'opracowanie', 'osiedle', 'pan', 'pani', 'panie',
                   'panowie', 'papieros', 'paragraf', 'parsek', 'państwo', 'pełniący_obowiązki', 'pikogram',
                   'piątek', 'piętro', 'plac', 'początek', 'podkomisarz', 'podporucznik', 'podpunkt',
                   'podpułkownik', 'pojemność', 'pokój', 'poniedziałek', 'porucznik', 'poseł', 'post_scriptum',
                   'posterunkowy', 'postscriptum', 'powiat', 'powierzchnia', 'pozycja', 'połowa', 'południe',
                   'praca', 'procent', 'profesor', 'projekt', 'projektant', 'prokurator', 'promil',
                   'prywatna_wiadomość', 'przebudowa', 'przed_naszą_erą', 'przyjazd', 'przypis', 'przypisek',
                   'pseudonim', 'punkt', 'pułk', 'pułkownik', 'północ', 'raz', 'redakcja', 'redaktor', 'refren',
                   'rezerwat', 'reżyseria', 'rotmistrz', 'rozdział', 'rycina', 'rysunek', 'rzeka', 'sekunda',
                   'senator', 'siostra', 'solidarność', 'spółka', 'spółka_akcyjna', 'spółka_cywilna', 'stopa',
                   'stopień', 'stowarzyszenie', 'strona', 'strony', 'sygnatura', 'szerokość', 'sztuka', 'tabela',
                   'telefon', 'temperatura', 'tom', 'towarzystwo', 'towarzystwo_funduszy_inwestycyjnych',
                   'towarzysz', 'towarzyszka', 'trade_mark', 'trybuna', 'tydzień', 'ubiegłego_roku',
                   'ubiegły_rok', 'ulica', 'uran', 'ustawa', 'ustęp', 'ułan', 'wartości_chrześcijańskie',
                   'water_closet', 'wejście', 'wezwanie', 'wiek', 'wschód', 'wkładka', 'województwo',
                   'wojna_światowa', 'wolt', 'wpierdol', 'zachód', 'zastępca', 'zdjęcie', 'zmiana', 'znak',
                   'związek', 'Ściana_Wschodnia', 'towarzystwo_funduszy_inwestycyjnych', 'wszechświat',
                   'wychowanie_fizyczne', 'wydanie', 'wyjście', 'wysokość', 'styczeń', 'luty', 'marzec',
                   'kwiecień', 'czerwiec', 'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad',
                   'grudzień', 'Anno_Domini', 'Immunoglobina_E', 'Jednostka_Wojskowa', 'Kodeks_Karny',
                   'Krzyż_Walecznych', 'Naczelna_Rada_Łowiecka',
                   'Polska_Organizacja_Narodowa_R.P._im._Mjr._H._Dobrzańskiego_"Hubala"', 'Saint', 'Solidarność',
                   'Spółka_Akcyjna', 'Sąd_Apelacyjny', 'Turbine_Steam_Ship', 'Wspólna_Polityka_Rybołówstwa',
                   'Zasadnicza_Szkoła', 'Dominikańskie_Centrum_Informacji_o_Sektach', 'Dzieje_Apostolskie',
                   'Dziennik_Ustaw', 'Ewangelia_wg_świętego_Łukasza', 'Ewangelia_świętego_Jana',
                   'Ewangelia_świętego_Marka', 'Ewangelia_świętego_Mateusza', 'Kościół_Katolicki',
                   'Kościół_Rzymskokatolicki', 'Księga_Ezechiela', 'Księga_Izajasza', 'Księga_Joela',
                   'Księga_Jonasza', 'Księga_Mądrości', 'Księga_Powtórzonego_Prawa', 'Księga_Samuela',
                   'Księga_Wyjścia', 'List_do_Efezjan', 'List_do_Kolosan', 'List_do_Koryntian', 'Nowy_Testament',
                   'Radio_Maryja', 'Stary_Testament', 'Wniebowzięcia_Najświętszej_Marii_Panny', 'arcybiskup',
                   'biskup', 'Ćwiczenia_Duchowe', 'Święty']:
        t.upos = 'NOUN'
    elif t.lemma in ['10-procentowy', '10-tysięczny', '2-procentowy', '30-procentowy', '400-tysięczny',
                     '5-procentowy', '50-procentowy', '7-procentowy', 'Gdański', 'Opolski', 'Wielki', 'akcyjny',
                     'angielski', 'bardzo', 'boży', 'były', 'centymetrowy', 'cesarsko-królewski',
                     'chrześcijański', 'dawny', 'dyskusyjny', 'ekonomiczny', 'elektryczny', 'gdański',
                     'geograficzny', 'gminny', 'grecki', 'habilitowany', 'inny', 'innymi', 'islandzki', 'karny',
                     'kaszubski', 'katolicki', 'kolejowy', 'kwadratowy', 'magnetyczny', 'maksymalny', 'minimalny',
                     'młodszy', 'najświętszy', 'nasz', 'nasza', 'niemiecki', 'odbudowany', 'parafialny',
                     'pięcioprocentowy', 'podstawowy', 'pojedynczy', 'polski', 'położony', 'południowy',
                     'procentowy', 'przebudowany', 'przeciwpancerny', 'północny', 'późniejszy', 'rozbudowany',
                     'różowy', 'społeczny', 'stumililitrowy', 'starszy', 'stary', 'stołeczny', 'szeregowy',
                     'sześcienny', 'ubiegły', 'urodzony', 'wagowy', 'wielki', 'wielkopolski', 'wielmożny',
                     'winien', 'wschodni', 'wyżej', 'wyżej_wymieniony', 'własna', 'własny', 'włoski', 'zachodni',
                     'zamieszkały', 'zawodowy', 'założony', 'zbudowany', 'zmarły', 'łaciński', 'średni',
                     'świętej_pamięci', 'święty', 'żółty', 'własna', 'większy_niż_lub_równy']:
        t.upos = 'ADJ'
    elif t.lemma in ['na_temat', 'do_spraw', 'koło', 'około', 'według']:
        t.upos = 'ADP'
    elif t.lemma in ['A', 'AF', 'B', 'C', 'Ch', 'Cz', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                     'P', 'Q', 'R', 'Rz', 'S', 'St', 'Sz', 'T', 'Th', 'U', 'V', 'W', 'X', 'Z', 'Ż', 'Adam',
                     'Agnieszka', 'Andrzej', 'Bernard', 'Borowski', 'Grażyna', 'Krystyna', 'Kublik', 'Marek',
                     'Mateusz', 'Małgorzata', 'Mister', 'Przełęcz', 'Stanisław', 'Tadeusz', 'Władysław', 'Zenon',
                     'Zygmunt', 'Gazeta_Wyborcza', 'Wiedza_i_Życie', 'Wiedza_i_życie', 'Wiedza_Życie',
                     'Rzeczpospolita', 'Rzeczpospolita_Polska', 'Trybuna', 'Trybuna_Ludu', 'Matka_Boska',
                     'Najświętsza_Maryja_Panna']:
        t.upos = 'PROPN'
    else:
        t.upos = 'ADV'


def frag(t: Token) -> None:
    """Converts a frag."""
    t.upos = 'X'
    if t.lemma not in ['dala', 'niemiara', 'naprzeciwka', 'ciemku', 'mimo', 'oścież', 'dwójnasób', 'wespół',
                       'oślep', 'trochu', 'młodu', 'cna', 'bezcen', 'dzieju', 'łupnia', 'mać', 'schwał',
                       'wskroś', 'wznak', 'zacz', 'przemian', 'zamian', '1a.']:
        t.ufeats = {'Foreign': 'Yes'}


def interp(t: Token) -> None:
    """Converts an interp."""
    t.upos = 'PUNCT'
    if t.lemma in ['[', '(', '⟨', '{']:
        t.ufeats = {'PunctType': 'Brck', 'PunctSide': 'Ini'}
    elif t.lemma in [']', ')', '⟩', '}']:
        t.ufeats = {'PunctType': 'Brck', 'PunctSide': 'Fin'}
    elif t.lemma == ':':
        t.ufeats = {'PunctType': 'Colo'}
    elif t.lemma == ',':
        t.ufeats = {'PunctType': 'Comm'}
    elif t.lemma in ['—', '- -', '--', '–', '‒', '―', '‐', '-']:
        t.ufeats = {'PunctType': 'Dash'}
    elif t.lemma == '…':
        t.ufeats = {'PunctType': 'Elip'}
    elif t.lemma == '!':
        t.ufeats = {'PunctType': 'Excl'}
    elif t.lemma == '.':
        t.ufeats = {'PunctType': 'Peri'}
    elif t.lemma == '?':
        t.ufeats = {'PunctType': 'Qest'}
    elif t.lemma == ';':
        t.ufeats = {'PunctType': 'Semi'}
    elif t.lemma in ['"', "'", '˝', '<<', '>>', '«', '»', "''"]:
        t.ufeats = {'PunctType': 'Quot'}
    elif t.lemma in ['„', '‘', '“']:
        t.ufeats = {'PunctType': 'Quot'}
        t.ufeats = {'PunctSide': 'Ini'}
    elif t.lemma in ['”', '’', '’’']:
        t.ufeats = {'PunctType': 'Quot'}
        t.ufeats = {'PunctSide': 'Fin'}
    elif t.lemma in ['/', '⁄']:
        t.ufeats = {'PunctType': 'Slsh'}
    elif t.lemma == '\\':
        t.ufeats = {'PunctType': 'Blsh'}


def xxx(t: Token) -> None:
    """Converts a xxx."""
    t.upos = 'X'
    t.ufeats = {'Foreign': 'Yes'}


def dig(t: Token) -> None:
    """Converts a dig."""
    t.upos = 'X'
    t.ufeats = {'NumForm': 'Digit'}


def romandig(t: Token) -> None:
    """Converts a romandig."""
    t.upos = 'X'
    t.ufeats = {'NumForm': 'Roman'}


def ign(t: Token) -> None:
    """Converts an ign."""
    t.upos = 'X'
    t.ufeats = {'Foreign': 'Yes'}


def sym(t: Token) -> None:
    """Converts a sym."""
    t.upos = 'SYM'


def incert(t: Token) -> None:
    """Converts an incert."""
    t.upos = 'X'
