# Konwersja tagów MPDT → UD

## 0. Funkcje pomocnicze

```f(gender)```:
- `manim1` &rArr; `Gender=Masc`, `Animacy=Hum`, `Number=<number>`
- `manim2` &rArr; `Gender=Masc`, `Animacy=Nhum`, `Number=<number>`
- `m` &rArr; `Gender=Masc`, `Number=<number>`
- `f` &rArr; `Gender=Fem`, `Number=<number>`
- `n` &rArr; `Gender=Neut`, `Number=<number>`
- `p1` &rArr; `Gender=Masc`, `Animacy=Hum`, `Number=Ptan`
- `p2` &rArr; `Gender=Neut`, `Number=Ptan`

```re_arabic``` finds Arabic numerals

```re_roman``` finds Roman numerals

## 1. Zamiana z podziałem na części mowy (POS tags)

lemma_based_upos -> pos_specific_upos

### 1.0. lemma_based_upos

- niż, niżeli, aniżeli, niźli, jakby, jakoby, niczym, niby && !subst && !part && !adv &rArr; `SCONJ` + `ConjType=Comp`
- jak &&  !subst &&  !conj &&  !adv &rArr; `SCONJ` + xpos = comp ????
- temu &rArr; `ADP` + `AdpType=Post,Case=Acc`
- plus, minus && !subst &rArr; `CCONJ` + `ConjType=Oper`
- !subst && !ign && re_arabic &rArr; ^^^ [num](#121-num-liczebnik-główny) + `NumType=Card` ^^^
- !subst && !ign && re_roman &rArr; ^^^ [num](#121-num-liczebnik-główny) + `NumType=Card` ^^^
- first letter upper &rArr; 

### 1.1. Rzeczowniki

#### 1.1.1. subst (rzeczownik)
Format: `subst : number : case : gender [ : subgender ]`\
`subst : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 [ : pt ]`

- co, kto &rArr; `PRON` + `PronType=Int,Rel`
- któż, cóż &rArr; `PRON` + `PronType=Int`
- ktoś, ktokolwiek, coś, cokolwiek &rArr; `PRON` + `PronType=Ind`
- nikt, nic &rArr; `PRON` + `PronType=Neg`
- to, tamto &rArr; `PRON` + `PronType=Dem`
- wszyscy, wszystko &rArr; `PRON` + `PronType=Tot`
- _ &rArr; `NOUN`

`Case=<case>` + `f(gender)`

### 1.2. Liczebniki

#### 1.2.1. num (liczebnik główny)
Format: `num : number : case : gender`\
`num : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2`

`f(gender)` + `Case=<case>`

if not set in lemma_based_upos:
- ile, ileż, iluż &rArr; `DET` + `NumType=Card,PronType=Int`
- tyle, tyleż &rArr; `DET` + `NumType=Card,PronType=Dem`
- mało, niemało, mniej, najmniej, dużo, niedużo, wiele, niewiele, więcej, najwięcej, kilka, kilkanastie, kilkadziesiąt, kilkaset, parę, paręnaście, oba, parędziesiąt, nieco, sporo, trochę, ileś, ilekolwiek, pełno, dość, dosyć &rArr; `DET` + `PronType=Ind`
- _ &rArr; `NUM` + `NumForm=Word`


#### 1.2.2. numcol (liczebnik zbiorowy)
Format: `numcol : number : case : gender`\
`numcol : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2`

^^^ [num](#121-num-liczebnik-główny) ^^^

#### 1.2.3. adjnum (liczebnik przymiotnikowy)
Format: `adjnum : number : case : gender : degree`\
`adjnum : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : pos|com|sup`

 ^^^ [adj](#131-adj-przymiotnik-i-zaimek-przymiotny) + `NumType=Ord` ^^^

#### 1.2.4. advnum (przysłówek liczebnikowy)
Format: `advnum : number : case : gender : degree`\
`advnum : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : pos|com|sup`

 ^^^ [adv](#141-adv-przysłówek) + `NumType=Ord` ^^^

### 1.3. Przymiotniki

#### 1.3.1. adj (przymiotnik i zaimek przymiotny)
Format: `adj : number : case : gender : degree`\
`adj : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : pos|com|sup`\
np. "którzy", "chwalebne"

- jaki, który &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Int,Rel`
- czyj, czyjże &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Int`
- któryż, jakiż &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Emp`
- któryś, którykolwiek, jakiś, jakikolwiek, niejaki, niektóry, niejeden, pewien &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Ind`
- każdy, wszelki, wszystek &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Tot`
- czyjś, czyjkolwiek &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Ind`
- żaden &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Neg`
- niczyj &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Neg`
- mój &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Prs,Number[psor]=Sing,Person=1`
- twój &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Prs,Number[psor]=Sing,Person=2`
- swój &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Prs`
- nasz &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Prs,Number[psor]=Plur,Person=1`
- wasz &rArr; `DET` + `Case=<case>` + `f(gender)` + `Poss=Yes,PronType=Prs,Number[psor]=Plur,Person=2`
- ten, tamten, ów, taki, takiż, tenże &rArr; `DET` + `Case=<case>` + `f(gender)` + `PronType=Dem`
- _ &rArr; `ADJ` + `Case=<case>` + `f(gender)` + `Degree=<degree>`

#### 1.3.2. adja (przymiotnik przyprzymiotnikowy)
Format: `adja`\
np. "biało" w "biało-czerwona"

`ADJ` + `Hyph=Yes`

#### 1.3.3. adjb (przymiotnik w odmianie niezłożonej)
Format: `adjb : number : case : gender : degree`\
`adjb : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : pos|com|sup`

^^^ [adj](#131-adj-przymiotnik-i-zaimek-przymiotny) + `Variant=Short` ^^^

### 1.4. Przysłówki

#### 1.4.1. adv (przysłówek)
Format: `adv : degree`\
`adv : pos|com|sup`

`ADV` + `Degree=<degree>` +
- (&not;rzadko) (kiedy|gdzie) (&not;indziej), skąd, dokąd, (&not;o) (ile) &rArr; `PronType=Int,Rel`
- jak && `degree != sup`, dokądś, dokądkolwiek, skądś, skądkolwiek, gdzieś, gdziekolwiek, jakoś, jakkolwiek, kiedyś, kiedykolwiek, którędyś, którędykolwiek, niekiedy, gdzieniegdzie &rArr; `PronType=Ind`
- tak, tu, tutaj, tam, ówdzie, stąd, stamtąd, tędy, wówczas, wtenczas, odtąd, dotąd, dlatego &rArr; `PronType=Dem`
- nigdy, nigdzie &rArr; `PronType=Neg`
- zawsze, wszędzie, zewsząd &rArr; `PronType=Tot`
- dlaczego, czemu, odkąd, którędy, dlaczegoż, dlaczegóż, czemuż, dokądże, skądże, jakże, którędyż, gdzież, kiedyż &rArr; `PronType=Int`

### 1.5. Zaimki

#### 1.5.1. ppron12 (zaimek osobowy nietrzecioosobowy)
Format: `ppron12 : number : case : person [ : accentability ]`\
`ppron12 : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : pri|sec [ : akc|nakc|neut|zneut ]`

`PRON` + `f(gender)` + `PronType=Prs,Case=<case>,Person=<person>`

- `akc` &rArr; `Variant=Long`
- _ &rArr; `Variant=Short`


#### 1.5.2. ppron3 (zaimek osobowy trzecioosobowy)
Format: `ppron3 : number : case : gender : person [ : accentability ] [ : post-prepositionality ]`\
`ppron3 : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : ter [ : akc|nakc|neut|zneut ] [ : npraep|praep ]`

`PRON` + `f(gender)` + `PronType=Prs,Case=<case>,Person=<person>`

- `akc` &rArr; `Variant=Long`
- _ &rArr; `Variant=Short`

#### 1.5.3. siebie (zaimek osobowy wzajemny)
Format: `siebie : case`\
`siebie : nom|gen|dat|acc|inst|loc|voc`

`PRON` + `PronType=Prs,Case=<case>,Reflex=Yes`

### 1.6. Przyimki

#### 1.6.1. prep (przyimek)
Format: `prep : case [ : vocalicity ]`\
`prep : nom|gen|dat|acc|inst|loc|voc [ : nwok|wok ]`

`ADP` + `Case=<case>` + `AdpType=Prep`
- `wok` &rArr; `Variant=Long`
- _ &rArr; `Variant=Short`

### 1.7. Spójniki

#### 1.7.1. conj (spójnik współrzędny)
Format: `conj`

`CCONJ`

#### 1.7.2. comp (spójnik podrzędny)
Format: `comp`

`SCONJ`

### 1.8. Partykuły

#### 1.8.1. part (partykuła)
Format: `part : vocalicity`\
`part : nwok|wok`

- się &rArr; `PRON` + `PronType=Prs,Reflex=Yes`
- by, niech, niechaj, niechże, niechby &rArr; `AUX`
- nie &rArr; `PART` + `Polarity=Neg`
- czy, czyż, czyżby, azaliż &rArr; `PART` + `PartType=Int`
- może &rArr; `PART` + `PartType=Mod`
- _ &rArr; `PART`

### 1.9. Wykrzykniki

#### 1.9.1. interj (wykrzyknik)
Format: `interj`

`INTJ`

### 1.10. Czasowniki

#### 1.10.1. fin (czasownik w formie nieprzeszłej)
Format: `fin : number : person : aspect`\
`fin : sg|du|pl : pri|sec|ter : perf|imperf|biasp`

- być, bywać &rArr; `AUX` + `Aspect=<aspect>,Number=<number>,Person=<person>,VerbForm=Fin`
- _ &rArr; `VERB` + `Aspect=<aspect>,Number=<number>,Person=<person>,VerbForm=Fin`

#### 1.10.2. bedzie (forma przyszła czasownika być)
Format: `bedzie : number : person : aspect`\
`bedzie : sg|du|pl : pri|sec|ter : perf|imperf|biasp`

`VERB` + `Aspect=<aspect>,Number=<number>,Person=<person>,VerbForm=Fin,Mood=Imp,Voice=Act`

#### 1.10.3. praet (pseudoimiesłów)
Format: `praet : number : gender : aspect [ : agglutination ]`\
`praet : sg|du|pl : f|n|m : perf|imperf|biasp [ : agl|nagl ]`

- być, bywać &rArr; `AUX` + `f(gender)` + `Aspect=<aspect>,VerbForm=Fin,Tense=Past,Voice=Act,Mood=Ind`
- _ &rArr; `VERB` + `f(gender)` + `Aspect=<aspect>,VerbForm=Fin,Tense=Past,Voice=Act,Mood=Ind`

#### 1.10.4. impt (rozkaźnik)
Format: `impt : number : person : aspect`\
`impt : sg|du|pl : pri|sec|ter : perf|imperf|biasp`

- być, bywać &rArr; `AUX` + `Aspect=<aspect>,VerbForm=Fin,Number=<number>,Person=<person>,Mood=Imp,Voice=Act`
- _ &rArr; `VERB` + `Aspect=<aspect>,VerbForm=Fin,Number=<number>,Person=<person>,Mood=Imp,Voice=Act`

#### 1.10.5. imps (bezosobnik)
Format: `imps : aspect`\
`imps : perf|imperf|biasp`

`VERB` + `Aspect=<aspect>,Mood=Ind,Person=0,Tense=Past,VerbForm=Fin,Voice=Act`

#### 1.10.6. inf (bezokolicznik)
Format: `inf : aspect`\
`inf : perf|imperf|biasp`

- być, bywać &rArr; `AUX` + `Aspect=<aspect>,VerbForm=Inf,Voice=Act`
- _ &rArr; `VERB` + `Aspect=<aspect>,VerbForm=Inf,Voice=Act`

#### 1.10.7. ger (odsłownik, gerundium)
Format: `ger : number : case : gender : aspect : negation`\
`ger : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m : perf|imperf|biasp : aff|neg`

`NOUN` + `f(gender)` + `Case=<case>,Aspect=<aspect>,Polarity=<negation>,VerbForm=Vnoun`

#### 1.10.8. pcon (imiesłów przysłówkowy współczesny)
Format: `pcon : aspect`\
`pcon : imperf`

- być, bywać &rArr; `AUX` + `Aspect=<aspect>,VerbForm=Conv,Voice=Act,Tense=Pres`
- _ &rArr; `VERB` + `Aspect=<aspect>,VerbForm=Conv,Voice=Act,Tense=Pres`

#### 1.10.9. pant (imiesłów przysłówkowy uprzedni)
Format: `pant : aspect`\
`pant : perf|imperf|biasp`

- być, bywać &rArr; `AUX` + `Aspect=<aspect>,VerbForm=Conv,Voice=Act,Tense=Past`
- _ &rArr; `VERB` + `Aspect=<aspect>,VerbForm=Conv,Voice=Act,Tense=Past`

#### 1.10.10. pact (imiesłów przymiotnikowy czynny)
Format: `pact : number : case : gender : aspect : negation : degree`\
`pact : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : imperf : aff|neg : pos|com|sup`

`ADJ` + `f(gender)` + `Case=<case>,Aspect=<aspect>,Polarity=<negation>,VerbForm=Part,Voice=Act`

#### 1.10.11. pactb (imiesłów przymiotnikowy odmieniony niezłożonie)
Format: ??? (brak wystąpień)

^^^ [pact](#11010-pact-imiesłów-przymiotnikowy-czynny) + `Variant=Short` ^^^

#### 1.10.12. ppas (imiesłów przymiotnikowy bierny)
Format: `ppas : number : case : gender : aspect : negation : degree`\
`ppas : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : perf|imperf|biasp : aff|neg : pos|com|sup`

`ADJ` + `f(gender)` + `Case=<case>,Aspect=<aspect>,Polarity=<negation>,VerbForm=Part,Voice=Pass`

#### 1.10.13. ppasb (imiesłów przymiotnikowy bierny odmieniony niezłożonie)
Format: `ppasb : number : case : gender : aspect : negation : degree`\
`ppasb : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : perf|imperf|biasp : aff|neg : pos|com|sup`

^^^ [ppas](#11012-ppas-imiesłów-przymiotnikowy-bierny) + `Variant=Short` ^^^

#### 1.10.14. ppraet (imiesłów przeszły)
Format: `ppraet : number : case : gender : aspect : negation`\
`ppraet : sg|du|pl : nom|gen|dat|acc|inst|loc|voc : f|n|m|p1|p2|manim1|manim2 : perf|imperf|biasp : aff|neg`

^^^ [ppas](#11012-ppas-imiesłów-przymiotnikowy-bierny) ^^^

#### 1.10.15. fut (czasownik być jako wykładnik czasu przyszłego)
Format: `fut : number : person : aspect`\
`fut : sg|du|pl : pri|sec|ter : perf|imperf|biasp`

`AUX` + `Aspect=<aspect>,VerbForm=Fin,Number=<number>,Person=<person>,Mood=Ind,Tense=Fut`

#### 1.10.16. plusq (czasownik być jako wykładnik czasu zaprzeszłego)
Format: `plusq : number : gender : aspect`\
`plusq : sg|du|pl : f|n|m|p1|p2|manim1|manim2 : perf|imperf|biasp`

- być, bywać &rArr; `AUX` + `f(gender)` + `Aspect=<aspect>,VerbForm=Fin,Tense=Past,Voice=Act,Mood=Ind`

#### 1.10.17. aglt (aglutynant)
Format: `aglt : number : person : aspect : vocalicity`\
`aglt : sg|du|pl : pri|sec|ter : perf|imperf|biasp : nwok|wok`

`AUX` + `Aspect=<aspect>,Number=<number>,Person=<person>`

- `wok` &rArr; `Variant=Short`
- _ &rArr; `Variant=Long`

#### 1.10.18. agltaor (aglutynant aorystyczny)
Format: `agltaor : number : person : aspect : vocalicity`\
`agltaor : sg|du|pl : pri|sec|ter : perf|imperf|biasp : nwok|wok`

^^^ [aglt](#11017-aglt-aglutynant) ^^^

#### 1.10.19. winien (czasownik typu wynien)
Format: `winien : number : gender : aspect`\
`winien : sg|du|pl : f|n|m|p1|p2|manim1|manim2 : perf|imperf|biasp`

`VERB` + `f(gender)` + `Aspect=<aspect>,VerbForm=Fin,Tense=Pres,Voice=Act,Mood=Ind,VerbType=Mod`

#### 1.10.20. pred (predykatyw)
Format: `pred`

- to &rArr; `AUX`
- _ &rArr; `VERB`

`Mood=Ind,Tense=Pres,VerbForm=Fin,VerbType=Quasi`

### 1.11. Inne

#### 1.11.1. brev (skrót)
Format: `brev : fullstoppedness`\
`brev : npun|pun`

- rok, stopień_Celsjusza, stopień_Fahrenheita, milimetr, milimetr_kwadratowy, milimetr_sześcienny,  centymetr, centymetr_kwadratowy, centymetr_sześcienny, cubic_centimetre, decymetr, decymetr_kwadratowy, decymetr_sześcienny, metr,metr_kwadratowy, metr_sześcienny, kilometr, kilometr_kwadratowy, kilometr_sześcienny,mikrometr, hektar, dekagram, gram, miligram, mikrogram, kilogram, megagram,Celsjusz, Celsjusza, bilion, miliard,  mililitr, milimetr, milion, gigadżul,gigaherc, kiloherc, megaherc, kilobajt, kilobajt_na_sekundę, gigabajt, megabajt,megabajt_na_sekundę, kilobit, milimol, megawat, kilowolt, kwintal, litr, mach,gaus, nanometr, tesla, tona, tysiąc,euro, jen, funt, dolar, złoty, nowy_polski_złoty, jen_japoński,dolar_amerykański, frank_belgijski, korona_duńska, United_States_Dollar, strona,aleja, aluminium, architekt, archiwum, artykuł, artysta, aspirant,bieżący_miesiąc, bieżący_rok,  brygada, centralne_ogrzewanie, ciąg_dalszy,ciąg_dalszy_nastąpi,  cytat,  cześć, departament, doba, docent, doktor, dolina,druh, dupa, dyrekcja, dyrektor, dywizja, dziennik, dzień, długość, editor,ekwiwalent_wodny, era, fotograf, fotografia, fundacja, generał, gmina, godzina,kilowatogodzina, grosz, głębokość, harcmistrz, hel, homoseksualista, hrabia,ilustracja, imienia, informacja, inspektor, inteligencja, inżynier,jednostka_miary, jezioro, junior, język, kapitan, kardynał, karta, kartka,kategoria, klasa, kleryk, kodeks, kodeks_postępowania_cywilnego,kodeks_prawa_cywilnego, kodeks_wykroczeń, kolega, komandor, komendant, komisarz,konstytucja, kopalnia, koło, koń_mechaniczny, kościół, kościół_katolicki, ksiądz,książę, lata, lekarz, liceum, liczba,  litera, magister, mecenas, medycyna,miara, miasto, miasto_stołeczne, miesiąc, miesięcy, mieszkanie, mieszkaniec,miligramorównoważnik, milijednostka, minimum, minister, ministerstwo, minuta,nadkomisarz, nadinspektor, nasza_era, naszej_ery, numer, objętość, obwód,oddział, odległość, odpowiedzialność, ograniczona_odpowiedzialność, ojciec,ojcowie, okolica, opatrzność, opracowanie, osiedle, pan, pani, panie,panowie, papieros, paragraf, parsek, państwo, pełniący_obowiązki, pikogram,piątek, piętro, plac, początek, podkomisarz, podporucznik, podpunkt,podpułkownik, pojemność, pokój, poniedziałek, porucznik, poseł, post_scriptum,posterunkowy, postscriptum, powiat, powierzchnia, pozycja, połowa,  południe,praca, procent, profesor, projekt, projektant, prokurator, promil,prywatna_wiadomość, przebudowa, przed_naszą_erą, przyjazd, przypis, przypisek,pseudonim, punkt, pułk, pułkownik, północ, raz, redakcja, redaktor, refren,rezerwat, reżyseria, rotmistrz, rozdział, rycina, rysunek, rzeka, sekunda,senator, siostra, solidarność, spółka, spółka_akcyjna, spółka_cywilna, stopa,stopień, stowarzyszenie, strona, strony, sygnatura, szerokość, sztuka, tabela,telefon, temperatura, tom, towarzystwo, towarzystwo_funduszy_inwestycyjnych,towarzysz, towarzyszka, trade_mark, trybuna, tydzień, ubiegłego_roku,ubiegły_rok, ulica, uran, ustawa, ustęp, ułan, wartości_chrześcijańskie,water_closet, wejście, wezwanie, wiek, wschód, wkładka, województwo,wojna_światowa, wolt, wpierdol, zachód, zastępca, zdjęcie, zmiana, znak,związek, Ściana_Wschodnia, towarzystwo_funduszy_inwestycyjnych, wszechświat,wychowanie_fizyczne, wydanie, wyjście, wysokość, styczeń, luty, marzec,kwiecień, czerwiec, lipiec, sierpień, wrzesień, październik, listopad,grudzień, Anno_Domini, Immunoglobina_E, Jednostka_Wojskowa, Kodeks_Karny,Krzyż_Walecznych, Naczelna_Rada_Łowiecka,Polska_Organizacja_Narodowa_R.P._im._Mjr._H._Dobrzańskiego_"Hubala", Saint, Solidarność,Spółka_Akcyjna, Sąd_Apelacyjny, Turbine_Steam_Ship, Wspólna_Polityka_Rybołówstwa,Zasadnicza_Szkoła, Dominikańskie_Centrum_Informacji_o_Sektach, Dzieje_Apostolskie,Dziennik_Ustaw, Ewangelia_wg_świętego_Łukasza, Ewangelia_świętego_Jana,Ewangelia_świętego_Marka, Ewangelia_świętego_Mateusza, Kościół_Katolicki,Kościół_Rzymskokatolicki, Księga_Ezechiela, Księga_Izajasza, Księga_Joela,Księga_Jonasza, Księga_Mądrości, Księga_Powtórzonego_Prawa, Księga_Samuela,Księga_Wyjścia, List_do_Efezjan, List_do_Kolosan, List_do_Koryntian,  Nowy_Testament,Radio_Maryja, Stary_Testament,  Wniebowzięcia_Najświętszej_Marii_Panny, arcybiskup,biskup, Ćwiczenia_Duchowe, Święty &rArr; `NOUN`
- 10-procentowy, 10-tysięczny, 2-procentowy, 30-procentowy, 400-tysięczny, 5-procentowy, 50-procentowy, 7-procentowy, Gdański, Opolski,  Wielki, akcyjny, angielski, bardzo, boży, były, centymetrowy, cesarsko-królewski, chrześcijański, dawny, dyskusyjny,  ekonomiczny, elektryczny, gdański, geograficzny,  gminny,  grecki, habilitowany, inny, innymi, islandzki, karny, kaszubski, katolicki, kolejowy, kwadratowy, magnetyczny, maksymalny, minimalny, młodszy, najświętszy, nasz, nasza, niemiecki, odbudowany, parafialny, pięcioprocentowy, podstawowy, pojedynczy, polski, położony, południowy, procentowy, przebudowany, przeciwpancerny, północny, późniejszy, rozbudowany, różowy,  społeczny, stumililitrowy, starszy, stary, stołeczny, szeregowy, sześcienny, ubiegły, urodzony, wagowy, wielki, wielkopolski, wielmożny, winien,  wschodni, wyżej, wyżej_wymieniony, własna, własny, włoski, zachodni, zamieszkały, zawodowy, założony, zbudowany,  zmarły, łaciński, średni, świętej_pamięci, święty, żółty, własna, większy_niż_lub_równy &rArr; `ADJ`
- na_temat, do_spraw, koło, około, według &rArr; `ADP`
- A, AF, B, C, Ch, Cz, D, E, F, G, H, I, J, K, L, M, N, O,P, Q, R, Rz, S, St, Sz, T, Th, U, V, W, X, Z, Ż, Adam,Agnieszka, Andrzej, Bernard, Borowski, Grażyna, Krystyna,  Kublik, Marek,Mateusz, Małgorzata, Mister, Przełęcz, Stanisław, Tadeusz, Władysław, Zenon,Zygmunt, Gazeta_Wyborcza, Wiedza_i_Życie, Wiedza_i_życie, Wiedza_Życie,Rzeczpospolita, Rzeczpospolita_Polska, Trybuna, Trybuna_Ludu, Matka_Boska,Najświętsza_Maryja_Panna &rArr; `PROPN`
- _ &rArr; `ADV`
`Abbr=Yes`

#### 1.11.2. frag (człon wyrażenia)
Format: `frag`

- dala, niemiara, naprzeciwka, ciemku, mimo, oścież, dwójnasób, wespół, oślep, trochu, młodu, cna, bezcen, dzieju, łupnia, mać, schwał, wskroś, wznak, zacz, przemian, zamian, 1a. &rArr; `X`
- _ &rArr; `X` + `Foreign=Yes`

#### 1.11.3. interp (znak interpunkcyjny)
Format: `interp`

`PUNCT`
- [ ( ⟨ { &rArr; `PunctType=Brck,PunctSide=Ini`
- ] ) ⟩ } &rArr; `PunctType=Brck,PunctSide=Fin`
- : &rArr; `PunctType=Colo`
- , &rArr; `PunctType=Comm`
- — - - -- – ‒ ― ‐ - &rArr; `PunctType=Dash`
- ... &rArr; `PunctType=Elip`
- ! &rArr; `PunctType=Excl`
- . &rArr; `PunctType=Peri`
- ? &rArr; `PunctType=Quest`
- ; &rArr; `PunctType=Semi`
- " ' ˝ << >> « » '' &rArr; `PunctType=Quot`
- „ ‘ “ &rArr; `PunctType=Quot,PunctSide=Ini`
- ” ’ ’’ &rArr; `PunctType=Quot,PunctSide=Fin`
- / ⁄ &rArr; `PunctType=Slsh`
- \ &rArr; `PunctType=Blsh`

#### 1.11.4. xxx (ciało obce)
Format: `xxx`

`X` + `Foreign=Yes`

#### 1.11.5. dig (zapis cyfrowy arabski)
Format: `dig`

`X` + `NumForm=Digit`

#### 1.11.6. romandig (zapis cyfrowy rzymski)
Format: `romandig`

`X` + `NumForm=Roman`

#### 1.11.7. ignndm (wyraz nieodmieniony o niejasnej funkcji)
Format: ??? (brak wystąpień)

#### 1.11.8. ign (wyraz o niejasnej funkcji i niejaslej lematyzacji)
Format: `ign`

`X` + `Foreign=Yes`

#### ???? 1.11.9. sym (symbol)
Format: `sym`

#### ???? 1.11.10. incert (nieokreślony)
Format: `incert`

`X`

## 2. Zależności

### 2.1. argumenty i inne podrzędniki predykatu

#### 2.1.1. adjunct (przydawka) - relacja między dowolną frazą pełniącą funkcję modyfikującą a modyfikowanym nadrzędnikiem

#### 2.1.2. adjunct_abl (okolicznik punktu początkowego)

#### 2.1.3. adjunct_adl (okolicznik punktu końcowego)

#### 2.1.4. adjunct_locat (okolicznik miejsca)

#### 2.1.5. adjunct_perl (okolicznik drogi)

#### 2.1.6. adjunct_temp (okolicznik czasu-terminu)

#### 2.1.7. adjunct_dur (okolicznik czasu trwania)

#### 2.1.8. adjunct_init (okolicznik momentu początku)

#### 2.1.9. adjunct_finit (okolicznik momentu końca)

#### 2.1.10. adjunct_freq (okolicznik częstotliwości)

#### 2.1.11. adjunct_mod (okolicznik sposobu)

#### 2.1.12. adjunct_instr (okolicznik instrumentu)

#### 2.1.13. adjunct_attit (okolicznik postawy)

#### 2.1.14. adjunct_caus (okolicznik przyczyny)

#### 2.1.15. adjunct_cond (okolicznik warunku)

#### 2.1.16. adjunct_concess (okolicznik przyzwolenia)

#### 2.1.17. adjunct_measure (okolicznik stopnia i miary)

#### 2.1.18. adjunct_purp (okolicznik celu)

#### 2.1.19. adjunct_result (okolicznik skutku)

#### 2.1.20. adjunct_substit (okolicznik zastąpienia)

#### 2.1.21. adjunct_refer (okolicznik względu)

#### 2.1.22. adjunct_attrib (okolicznik atrybutu)

#### 2.1.23. adjunct_compan (okolicznik towarzyszący)

#### 2.1.24. adjunct_recip (okolicznik odbiorcy)

#### 2.1.25. adjunct_other (okolicznik towarzyszący)

#### 2.1.26. adjunct_elect (konstrukcje elektywne)

#### 2.1.27. adjunct_title (tytuł)

#### 2.1.28. adjunct_comment (komentarz do sytuacji)

#### 2.1.29. adjunct_compar - relacja między strukturą porównawczą a jej nadrzędnikiem

#### 2.1.30. adjunct_emph - partykuła podkreślająca i uwydatniająca znaczenie danego wyrażenia

#### 2.1.31. aglt - aglutynant czasownika być (mobilny afiks), który może pojawić się w różnych pozycjach w ramach frazy zdaniowej

#### 2.1.32. aux - czasownik posiłkowy być lub zostać z nadrzędnym czasownikiem (albo głównym, albo quasi- w czasie przyszłym złożonym, konstrukcjach w analitycznym trybie warunkowym oraz w konstrukcjach w stronie biernej)

#### 2.1.33. comp podrzędnik wymagany (complement) - dopełnienie dalsze wyrażone nierzeczownikiem

#### 2.1.34. comp_ag podrzędnik będący semantycznym podmiotem w zdaniach w stronie biernej, realizowany przez wyrażenie przyimkowe z `przez`

#### 2.1.35. comp_fin - wymagane zdanie podrzędne

#### 2.1.36. comp_inf - podrzędnik wymagany realizowany jako dopełniająca fraza bezokolicznikowa

#### 2.1.37. cond - partykuła `by` w trybie przypuszczającym, której nadrzędnikiem jest pseudoimiesłów lub forma quasi-czasownikowa

#### 2.1.38. imp - partykuła `niech`, `niechże`, `niechajże`, której nadrzednikiem jest forma czasownikowa

#### 2.1.39. mark_rel - relacja między orzeczeniem zdania względnego i znacznikiem zdania względnego `co`

#### 2.1.40. neg - znacznik negacji `nie`, którego nadrzędnikiem jest czasownik lub inny składnik

#### 2.1.41. obj - dopełnienie bliższe z nadrzędnym czasownikiem

#### 2.1.42. obj_attrib - dopełnienie określające uczestnika sytuacji

#### 2.1.43. obj_caus - argument przyczyniający się do wykonania czynności

#### 2.1.44. obj_exper - argument odczuwający uczucia i emocje

#### 2.1.45. obj_instr - argument wspomagający akcję

#### 2.1.46. obj_manner - argument określający sposób wykonania czynności

#### 2.1.47. obj_measure - argument określający stopień / miarę / wielkość czynności

#### 2.1.48. obj_recip - argument będący odbiorcą czynności

#### 2.1.49. obj_result - argument będący wynikiem czynności lub powstający w jej skutek

#### 2.1.50. obj_stimul - argument, który swoją cechą lub właściwością wywołuje subiektywną reakcję

#### 2.1.51. obj_theme - argument podlegający samoistnemu procesowi, znajdujący się w jakimś stanie lub podlegający działaniu kogoś / czegoś, ale nie mający wpływu na ten proces

#### 2.1.52. pd - podrzędnik wymagany - odpowiada orzecznikowy, ryażonyu przez różne frazy; nadrzędnikiem jest predykatyw `to` lub `oto` oraz formy czasowników łącznikowych `być`, `bywać`, `czynić`, `okazać się`, `okazywać się`, `oznaczać`, `pozostać`, `pozostawać`, `roboc`, `stać się`, `stanowić`, `stawać się`, `ustanawiać`, `uznawać`, `wydać się`, `wydawać się`, `zdawać się`, `znaczyć`, `zostać`, `zostawać`, `zrobić się`

#### 2.1.53. refl - `się` lub `sobie` z czasownikiem

#### 2.1.54. subj - argument predykatu, podmiot

#### 2.1.55. vocative - relacja między predykatem zdania a rzeczownikiem w wołaczu

### 2.2 podrzędniki rzeczownika

#### 2.2.1. adjunct
^^^ [2.1.1. adjunct](#211-adjunct-przydawka) ^^^

#### 2.2.2. adjunct_compar
^^^ [2.1.29. adjunct_compar](#2129-adjunct_compar-relacja-między-strukturą-porównawczą-a-jej-nadrzędnikiem) ^^^

#### 2.2.3. adjunct_emph
^^^ [2.1.30. adjunct_emph](#2130-adjunct_emph-partykuła-podkreślająca-i-uwydatniająca-znaczenie-danego-wyrażenia) ^^^

#### 2.2.4. adjunct_poss - relacja między rzeczownikiem a wyrażeniuem posesywnym odpowiadającym na pytanie `czyj?`

#### 2.2.5. adjunct_rc - relacja między rzeczownikiem (czasem przysłówkiem) a predykatem zdania względnego lub predykatem zdania głównego a predykatem zdania względnego

#### 2.2.6. app - modyfikator apozycyjny rzeczownika - przydawka rzeczownikowa występująca bezpośrednio po pierwszym rzeczowniku i służąca do definiowania, modyfikowania, nazywania lub opisywania tego pierwszego rzeczownika

#### 2.2.7. comp - ^^^ [2.1.33. comp podrzędnik wymagany](#2133-comp-podrzędnik-wymagany-complement) ^^^

### 2.3. typy relacji w strukturach koordynacyjnych

#### 2.3.1. conjunct - koordynant, będący podrzędnikiem koordynatora (tj. spójnika współrzędnego lub odpowiadającego mu znaku interpunkcyjnego)

#### 2.3.2. pre_coord - odpowiednik spójnika współrzędnego lub pierwszy spójnik w spójniku szeregowym

### 2.4. typy relacji w jednostkach wielowyrazowych

#### 2.4.1. mwe - relacja między elementami morfoskładniowych jednostek wielowyrazowych

#### 2.4.2. ne - relacja pomiędzy elementami wielowyrazowych nazw własnych

#### 2.4.3. ne_foreign - relacja między sekwencją obcych słów a jej głową

nie ma w danych

### 2.5. typy relacji luźnych

#### 2.5.1. adjunct_qt - relacja między predykatem zdania głównego a zdaniem lub równoważnikiem zdania w mowie niezależnej

#### 2.5.2. item - znacznik (numer, litera, symbol) poszczególnych elementów listy, którego nadrzędnikiem jest składnik główny danego elementu

### 2.6. typy relacji specjalnych

#### 2.6.1. orphan - jeden z podrzędników przy elipsie jest oznaczany jako nadrzędnik, a pozostałe podrzędniki to orphan

#### 2.6.2. discourse - elementy pozajęzykowe, np. yy yyy yyyy y

nie ma w danych

#### 2.6.3. parataxis - relacja łącząca predykaty wszystkich zdań oprócz pierwszego z jednej tury z predykatem pierwszego zdania

#### 2.6.4. parataxis_restart - niedokończone frazy zastąpione nową frazą

nie ma w danych

#### 2.6.5. reparandum - poprawka będąca powtórzeniem, zastąpieniem lub przeformułowaniem

nie ma w danych

### 2.7. typy relacji interpunkcyjnych

#### 2.7.1 abbrev_punct - kropka w skrótach

#### 2.7.2 punct - znak interpunkcyjny niebędący koordynatorem

### 2.8. typy relacji pomocniczych

#### 2.8.1 dep - zależność nieokreślona

#### 2.8.2 root - relacja między korzeniem drzewa a jego podrzędnikiem

### 2.9. konwersja

#### 2.9.1. preconversion

- !root && `SCONJ` && jak, jakby && edge(gov(n), n) == `adjunct_compar` &rArr; n.`ConjType=Comp`
- `AUX` && !aglt && !cond && !children(n, `conj`) && !children(n, `cc`) && edge(gov(n), n) != `aux` && !to && !by && len(children(n)) > 0 && children(n, `adjunct_locat`) && !children(n, `pd`) &rArr; `VERB`
- `AUX` && !aglt && !cond && !children(n, `conj`) && !children(n, `cc`) && edge(gov(n), n) != `aux` && !to && !by && len(children(n)) > 0 && !children(n, `pd`) &rArr; `VERB`
- `AUX` && !aglt && !cond && !children(n) && być && edge(gov(n), n) != `aux` && edge(gov(n), n) != `aglt` && !edge(n, children(n, `conjunct`)) &rArr; `VERB`
- `AUX` && !aglt && !cond && !children(n) && być && edge(gov(n), n) != `aux` && edge(gov(n), n) != `aglt` && edge(gov(same_dep_branches_leaf(n)),same_dep_branches_leaf(n)) != `aux` && !children(n, `pd`) &rArr `VERB`
- `VERB` && edge(gov(n), n) == `aux` &rArr; `AUX`

#### conversion of <pos> = num
- children(n, `comp`) 

- 

## 3. Pytania / problemy

- obecnie ppron12 bez accentability idzie do Variant=Short razem z nakc, a ppron3 z neut,zneut idzie do Variant=Short razem z nakc, nie jestem tego pewien - sprawdzic

- NumType=Sets poczytać

- jej / jego

- przy 'bedzie' wcześniej było Tense=Fut, ale w nowym kodzie jest zamiast tego Voice=Act (wygląda na błędne użycie impt zamiast 'bedzie' ale może to celowo?)
- tu jest ok - dodaje sie tense tam gdzie ma byc

- czym są cneg, obj_factor, obj_purp? - nie ma ich w instrukcji do anotacji PDB
- cneg to negacja do fraz ktore sa nieczasownikowe

- xpos = comp do korektora

constituent negation	84 
obj_factor	4
obj_purp	6