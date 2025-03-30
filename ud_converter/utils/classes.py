"""
Module for the Sentence and Token classes.
"""
from collections import defaultdict
from typing import Dict, List
from utils.feats_dict import feats_dict
from utils.multiword_dict import MULTIWORD_EXPRESSIONS as MWE

class Sentence:
    """
    A Sentence holds a list of Node objects.
    It provides a get_root method returning the Node whose gov_id == "0".
    """

    def __init__(self, tokens: List['Token']) -> None:
        self.tokens: List['Token'] = tokens
        self.dict_by_id: Dict[str, 'Token'] = {token.id: token for token in tokens}
        self.meta = defaultdict(str)

        for token in tokens:
            token.sentence = self

    def get_root(self):
        """
        Returns the Token whose gov_id == '0' (i.e. the root).
        If for some reason there's no root, returns None.
        """
        for token in self.tokens:
            if token.gov_id == '0':
                return token
        return None

    @property
    def text(self) -> str:
        """Returns the text of the sentence."""
        return " ".join([token.form for token in self.tokens])

    @property
    def meta(self) -> Dict[str, str]:
        """Returns the metadata of the sentence."""
        return self.meta
    @meta.setter
    def meta(self, value: Dict[str, str]) -> None:
        """Sets the metadata of the sentence."""
        self.meta.update(value)

    def write_meta(self, out) -> None:
        """Writes the metadata of the sentence."""
        for key, value in self.meta.items():
            out.write(f"# {key} = {value}\n")

    def __str__(self) -> str:
        """Returns the sentence as its tokens joined by newline."""
        return "\n".join(str(token) for token in self.tokens)

    def __iter__(self):
        return iter(self.tokens)


class Token:
    """
    A token has its properties:
    id, form, lemma, pos, pos_feats, feats, gov_id, dep_label, sent_id, misc
    """
    def __init__(self, line: str) -> None:
        columns: List[str] = line.split("\t")
        self.sentence = None
        self.data = {}
        self.data['id'] = columns[0]
        self.data['form'] = columns[1]
        self.data['lemma'] = MWE.get(columns[2], columns[2])
        self.data['pos'] = columns[3]
        self.data['upos'] = ''
        self.data['pos_feats'] = columns[4]
        self.data['feats_raw'] = columns[5]
        self.data['feats'] = defaultdict(str)
        if self.data['feats_raw'] != "_":
            self.data['feats'] = {feats_dict[feat]: feat for feat in self.data['feats_raw'].split("|")}
        self.data['ufeats'] = defaultdict(str)
        self.data['gov_id'] = columns[6]
        self.data['gov'] = None
        self.data['dep_label'] = columns[7]
        self.data['udep_label'] = None
        self.data['sent_id'] = columns[8]
        self.data['misc'] = columns[9]
        self.data['umisc'] = defaultdict(str)
        self.data['umisc']['Translit'] = columns[9]

    @property
    def id(self) -> str:
        """Returns the id of the token."""
        return self.data['id']

    @id.setter
    def id(self, value: str) -> None:
        """Sets the id of the token."""
        self.data['id'] = value

    @property
    def form(self) -> str:
        """Returns the form of the token."""
        return self.data['form']

    @form.setter
    def form(self, value: str) -> None:
        """Sets the form of the token."""
        self.data['form'] = value

    @property
    def lemma(self) -> str:
        """Returns the lemma of the token."""
        return self.data['lemma']

    @lemma.setter
    def lemma(self, value: str) -> None:
        """Sets the lemma of the token."""
        self.data['lemma'] = value

    @property
    def pos(self) -> str:
        """Returns the pos of the token."""
        return self.data['pos']

    @pos.setter
    def pos(self, value: str) -> None:
        """Sets the pos of the token."""
        self.data['pos'] = value

    @property
    def pos_feats(self) -> str:
        """Returns the token's pos with its features."""
        return self.data['pos_feats']

    @pos_feats.setter
    def pos_feats(self, value: str) -> None:
        """Sets the token's pos with its features."""
        self.data['pos_feats'] = value

    @property
    def feats(self):
        """Returns a dictionary of feats for the token."""
        return self.data['feats']

    @feats.setter
    def feats(self, value: Dict[str, str]) -> None:
        """Sets the dictionary of feats for the token."""
        self.data['feats'] = value
        self.data['feats_raw'] = "|".join(value.values())

    @property
    def gov_id(self) -> str:
        """Returns the id of the governor of the token."""
        return self.data['gov_id']

    @gov_id.setter
    def gov_id(self, value: str) -> None:
        """Sets the id of the governor of the token."""
        self.data['gov_id'] = value

    @property
    def dep_label(self) -> str:
        """Returns the dependency label of the token."""
        return self.data['dep_label']

    @dep_label.setter
    def dep_label(self, value: str) -> None:
        """Sets the dependency label of the token."""
        self.data['dep_label'] = value

    @property
    def sent_id(self) -> str:
        """Returns the id of the sentence of the token."""
        return self.data['sent_id']

    @sent_id.setter
    def sent_id(self, value: str) -> None:
        """Sets the id of the sentence of the token."""
        self.data['sent_id'] = value

    @property
    def misc(self) -> str:
        """Returns the misc of the token."""
        return self.data['misc']

    @misc.setter
    def misc(self, value: str) -> None:
        """Sets the misc of the token."""
        self.data['misc'] = value

    @property
    def umisc(self):
        """Returns the UD misc of the token."""
        return self.data['umisc']

    @umisc.setter
    def umisc(self, value: Dict[str, str]) -> None:
        """Updates the UD misc of the token."""
        self.data['umisc'].update(value)

    @property
    def feats_raw(self) -> str:
        """Returns the raw feats of the token."""
        return self.data['feats_raw']

    @feats_raw.setter
    def feats_raw(self, value: str) -> None:
        """Sets the raw feats of the token."""
        self.data['feats_raw'] = value
        self.data['feats'] = {feats_dict[feat]: feat for feat in value.split("|")}

    @property
    def upos(self) -> str:
        """Returns the upos of the token."""
        return self.data['upos']

    @upos.setter
    def upos(self, value: str) -> None:
        """Sets the upos of the token."""
        self.data['upos'] = value

    @property
    def ufeats(self):
        """Returns the ufeats of the token."""
        return self.data['ufeats']

    @ufeats.setter
    def ufeats(self, value: Dict[str, str]) -> None:
        """Updates the ufeats of the token."""
        self.data['ufeats'].update(value)

    @property
    def udep_label(self):
        """Returns the udep_label of the token."""
        return self.data['udep_label']

    @udep_label.setter
    def udep_label(self, value: Dict[str, str]) -> None:
        """Sets the udep_label of the token."""
        self.data['udep_label'] = value

    def __str__(self) -> str:
        """
        Returns the Token as a line in UD CONLL-U format.
        Columns: ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC.
        For FEATS, if no features are present, outputs '_'. DEPS is set to '_'.
        """
        upos_str = self.data['upos'] if self.data['upos'] else self.data['pos']
        feats_str = self.data['feats_raw'] if not self.data['upos'] else "|".join([f"{key}={value}" for key, value in self.data['ufeats'].items()])
        misc_str = self.data['misc'] if not self.data['upos'] else "|".join([f"{key}={value}" for key, value in self.data['umisc'].items()])

        return "\t".join([
            self.data['id'],
            self.data['form'],
            self.data['lemma'],
            upos_str,
            self.data['pos_feats'],
            feats_str,
            self.data['gov_id'],
            self.data['dep_label'],
            self.data['sent_id'],
            misc_str
        ])

    @property
    def gov(self):
        """Returns the governor Token, or None if it's the root or something is missing."""
        if self.sentence is None:
            return None
        if self.gov_id == "0":
            return None
        return self.sentence.dict_by_id.get(self.gov_id)

    @property
    def children(self) -> List['Token']:
        """
        Returns a list of tokens for which this token is the governor.
        If there are no children, returns an empty list.
        """
        if self.sentence is None:
            return []
        return [
            n for n in self.sentence.tokens
            if n.gov_id == self.id
        ]

    @property
    def prev(self):
        """Returns the previous token in the sentence."""
        if self.sentence is None:
            return None
        return self.sentence.dict_by_id.get(str(int(self.id) - 1), None)

    @property
    def next(self):
        """Returns the next token in the sentence."""
        if self.sentence is None:
            return None
        return self.sentence.dict_by_id.get(str(int(self.id) + 1), None)
