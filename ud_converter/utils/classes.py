"""
Module for the Sentence and Token classes.
"""
from collections import defaultdict
from typing import Dict, List
from utils.constants import feats_dict, MULTIWORD_EXPRESSIONS as MWE


class Sentence:
    """
    A Sentence holds a list of Node objects.
    It provides a get_root method returning the Node whose gov_id == "0".
    """

    def __init__(self, tokens: List['Token']) -> None:
        self.tokens: List['Token'] = tokens
        self.dict_by_id: Dict[str, 'Token'] = {token.id: token for token in tokens}
        self.metadata = defaultdict(str)

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
        if 'text' in self.metadata:
            return self.metadata['text']
        return " ".join(token.form for token in self.tokens)

    @property
    def meta(self) -> Dict[str, str]:
        """Returns the metadata of the sentence."""
        return self.metadata

    @meta.setter
    def meta(self, value: Dict[str, str]) -> None:
        """Sets the metadata of the sentence."""
        self.metadata.update(value)

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
        if line != 'mwe':
            columns: List[str] = line.split("\t")
            self.sentence = None
            self.data = {}
            self.data['id'] = columns[0]
            self.data['form'] = columns[1]
            self.data['lemma'] = MWE.get(columns[2], columns[2])
            self.data['pos'] = columns[3]
            self.data['upos'] = ''
            self.data['pos_feats'] = columns[4]
            self.data['feats_raw'] = columns[5] if columns[5]  != '' else '_'
            self.data['feats'] = defaultdict(str)
            if self.data['feats_raw'] != "_":
                self.data['feats'] = {feats_dict[feat]: feat for feat in self.data['feats_raw'].split("|")}
            self.data['ufeats'] = defaultdict(str)
            self.data['gov_id'] = columns[6]
            self.data['ugov_id'] = None
            self.data['gov'] = None
            self.data['ugov'] = None
            self.data['dep_label'] = columns[7]
            self.data['udep_label'] = ''
            self.data['sent_id'] = columns[8]
            self.data['misc'] = columns[9]
            self.data['umisc'] = defaultdict(str)
            self.data['umisc']['Translit'] = columns[9]
        else:
            self.sentence = None
            self.data = {}
            self.data['id'] = '_'
            self.data['form'] = '_'
            self.data['lemma'] = '_'
            self.data['pos'] = '_'
            self.data['upos'] = '_'
            self.data['pos_feats'] = '_'
            self.data['feats_raw'] = '_'
            self.data['feats'] = defaultdict(str)
            self.data['ufeats'] = defaultdict(str)
            self.data['gov_id'] = '_'
            self.data['ugov_id'] = None
            self.data['gov'] = None
            self.data['ugov'] = None
            self.data['dep_label'] = '_'
            self.data['udep_label'] = '_'
            self.data['sent_id'] = '_'
            self.data['misc'] = '_'
            self.data['umisc'] = defaultdict(str)
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
    def ugov_id(self) -> str:
        """Returns the id of the governor of the token."""
        return self.data['ugov_id']

    @ugov_id.setter
    def ugov_id(self, value: str) -> None:
        """Sets the id of the governor of the token."""
        self.data['ugov_id'] = value

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
        if self.data['upos'] == '':
            upos_str = self.data['pos']
            feats_str = self.data['feats_raw']
            sent_str = self.data['sent_id']
            misc_str = self.data['misc']
        else:
            upos_str = self.data['upos']
            feats_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['ufeats'].items())]) if self.data['ufeats'] else '_'
            sent_str = '_'
            misc_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['umisc'].items())]) if self.data['umisc'] else '_'

        return "\t".join([
            self.data['id'],
            self.data['form'],
            self.data['lemma'],
            upos_str,
            self.data['pos_feats'],
            feats_str,
            self.data['gov_id'],
            self.data['dep_label'],
            sent_str,
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
    def ugov(self):
        """Returns the governor Token, or None if it's the root or something is missing."""
        if self.sentence is None:
            return None
        if self.ugov_id == "0":
            return None
        return self.sentence.dict_by_id.get(self.ugov_id)

    @ugov.setter
    def ugov(self, value: 'Token') -> None:
        """Sets the governor Token."""
        self.ugov_id = value.id

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

    @property
    def children_with_label(self, label: str) -> List['Token']:
        """Returns a list of children of the token with the given dependency label."""
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if n.dep_label == label
        ]

    @property
    def children_with_lemma(self, lemma: str) -> List['Token']:
        """Returns a list of children of the token with the given lemma."""
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if n.lemma == lemma
        ]

    @property
    def rec_gov_via_label(self, label: str) -> 'Token':
        """
        Returns the governor of the token if the dependency label is == label, and gov's gov is != label. 
        If there is no such governor, returns None.
        If the governor's governor is == label, returns the governor's governor, etc.
        """
        if self.sentence is None:
            return None
        if self.dep_label == label:
            if self.gov.dep_label != label:
                return self.gov
            else:
                return self.gov.rec_gov_via_label(label)
        return None

    @property
    def rec_child_with_label_via_label(self, target_label: str, label: str) -> 'Token':
        """
        Returns the child of the token with the given dependency label.
        If there is no such child, goes through the children's children with the given label and looks for the target label.
        If a child is found, return it.
        If no child is found, returns None.
        """
        if self.sentence is None:
            return None
        if self.dep_label == label:
            for child in self.children:
                if child.dep_label == target_label:
                    return child
                else:
                    return child.rec_child_with_label_via_label(target_label, label)
        return None
