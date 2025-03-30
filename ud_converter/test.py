from utils.io import read_conll
from utils.classes import Token, Sentence
from morphosyntax.postconversion import post_conversion

all_sentences = read_conll("data/MPDT/MPDT_1.conll")

# for i, sent in enumerate(all_sentences, start=1):
#     print(f'Sentence {i}, root = {sent.get_root().form if sent.get_root() else "(no root)"}')
#     print([child.form for child in sent.get_root().children])

meta = {
    "sent_id": "1015",
    "text": ("I ciebie/ i siebiebym wielce zabawił; gdybym wszystkie świadectwa i zdania o tym/ "
             "ludzi poważnych/ chciał tu przytoczyć."),
    "orig_file_sentence": "SekrWyj#morph_1.262-s",
    "text_translit": ("I ćiebie/ i siebiebym wielce zábáwił; gdybym wszystkie świádectwá i zdániá o tym/ "
                       "ludzi powáżnych/ chćiał tu przytoczyć.")
}

"""
1	I	i	conj	conj	_	4	pre_coord	2735	I
2	ciebie	ty	ppron12	ppron12:sg:acc:sec:akc	sg|acc|sec|akc	4	conjunct	2735	ćiebie
3	/	/	interp	interp	_	4	punct	2735	/
4	i	i	conj	conj	_	9	obj	2735	i
5	siebie	siebie	siebie	siebie:acc	acc	4	conjunct	2735	siebie
6	by	by	part	part	_	9	cond	2735	by
7	m	być	aglt	aglt:sg:pri:imperf:nwok	sg|pri|imperf|nwok	6	aglt	2735	m
8	wielce	wielce	adv	adv:pos	pos	9	adjunct_measure	2735	wielce
9	zabawił	zabawić	praet	praet:sg:m:perf	sg|m|perf	0	root	2735	zábáwił
10	;	;	interp	interp	_	11	punct	2735	;
11	gdyby	gdyby	comp	comp	_	9	adjunct_cond	2735	gdyby
12	m	być	aglt	aglt:sg:pri:imperf:nwok	sg|pri|imperf|nwok	11	aglt	2735	m
13	wszystkie	wszystek	adj	adj:pl:acc:n:pos	pl|acc|n|pos	15	adjunct	2735	wszystkie
14	świadectwa	świadectwo	subst	subst:pl:acc:n	pl|acc|n	15	conjunct	2735	świádectwá
15	i	i	conj	conj	_	25	obj	2735	i
16	zdania	zdanie	subst	subst:pl:acc:n	pl|acc|n	15	conjunct	2735	zdániá
17	o	o	prep	prep:loc	loc	15	comp	2735	o
18	tym	to	subst	subst:sg:loc:n	sg|loc|n	17	comp	2735	tym
19	/	/	interp	interp	_	20	punct	2735	/
20	ludzi	człowiek	subst	subst:pl:gen:m	pl|gen|m	15	adjunct	2735	ludzi
21	poważnych	poważny	adj	adj:pl:gen:m:pos	pl|gen|m|pos	20	adjunct	2735	powáżnych
22	/	/	interp	interp	_	20	punct	2735	/
23	chciał	chcieć	praet	praet:sg:m:imperf	sg|m|imperf	11	comp_fin	2735	chćiał
24	tu	tu	adv	adv	_	25	adjunct_locat	2735	tu
25	przytoczyć	przytoczyć	inf	inf:perf	perf	23	comp_inf	2735	przytoczyć
26	.	.	interp	interp	_	9	punct	2735	.
"""
# Token lines (using tab-separated fields, as in your example)
token_lines = [
    "1\tI\ti\tconj\tconj\t_\t4\tpre_coord\t2735\tI",
    "2\tciebie\tty\tppron12\tppron12:sg:acc:sec:akc\tsg|acc|sec|akc\t4\tconjunct\t2735\tćiebie",
    "3\t/\t/\tinterp\tinterp\t_\t4\tpunct\t2735\t/",
    "4\ti\ti\tconj\tconj\t_\t9\tobj\t2735\ti",
    "5\tsiebie\tsiebie\tsiebie\tsiebie:acc\tacc\t4\tconjunct\t2735\tsiebie",
    "6\tby\tby\tpart\tpart\t_\t9\tcond\t2735\tby",
    "7\tm\tbyć\taglt\taglt:sg:pri:imperf:nwok\tsg|pri|imperf|nwok\t6\taglt\t2735\tm",
    "8\twielce\twielce\tadv\tadv:pos\tpos\t9\tadjunct_measure\t2735\twielce",
    "9\tzabawił\tzabawić\tpraet\tpraet:sg:m:perf\tsg|m|perf\t0\troot\t2735\tzábáwił",
    "10\t;\t;\tinterp\tinterp\t_\t11\tpunct\t2735\t;",
    "11\tgdyby\tgdyby\tcomp\tcomp\t_\t9\tadjunct_cond\t2735\tgdyby",
    "12\tm\tbyć\taglt\taglt:sg:pri:imperf:nwok\tsg|pri|imperf|nwok\t11\taglt\t2735\tm",
    "13\twszystkie\twszystek\tadj\tadj:pl:acc:n:pos\tpl|acc|n|pos\t15\tadjunct\t2735\twszystkie",
    "14\tświadectwa\tświadectwo\tsubst\tsubst:pl:acc:n\tpl|acc|n\t15\tconjunct\t2735\tświádectwá",
    "15\ti\ti\tconj\tconj\t_\t25\tobj\t2735\ti",
    "16\tzdania\tzdanie\tsubst\tsubst:pl:acc:n\tpl|acc|n\t15\tconjunct\t2735\tzdániá",
    "17\to\to\tprep\tprep:loc\tloc\t15\tcomp\t2735\to",
    "18\ttym\tto\tsubst\tsubst:sg:loc:n\tsg|loc|n\t17\tcomp\t2735\ttym",
    "19\t/\t/\tinterp\tinterp\t_\t20\tpunct\t2735\t/",
    "20\tludzi\tczłowiek\tsubst\tsubst:pl:gen:m\tpl|gen|m\t15\tadjunct\t2735\tludzi",
    "21\tpoważnych\tpoważny\tadj\tadj:pl:gen:m:pos\tpl|gen|m|pos\t20\tadjunct\t2735\tpowáżnych",
    "22\t/\t/\tinterp\tinterp\t_\t20\tpunct\t2735\t/",
    "23\tchciał\tchcieć\tpraet\tpraet:sg:m:imperf\tsg|m|imperf\t11\tcomp_fin\t2735\tchćiał",
    "24\ttu\ttu\tadv\tadv\t_\t25\tadjunct_locat\t2735\ttu",
    "25\tprzytoczyć\tprzytoczyć\tinf\tinf:perf\tperf\t23\tcomp_inf\t2735\tprzytoczyć",
    "26\t.\t.\tinterp\tinterp\t_\t9\tpunct\t2735\t."
]

tokens = [Token(line) for line in token_lines]
sentence = Sentence(tokens)
sentence.meta = meta
post_conversion(sentence)
for t in sentence.tokens:
    print(str(t))
