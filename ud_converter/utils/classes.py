"""
Module containing the Sentence and Token classes used throughout the UD Converter project.

This module defines the core data structures for representing sentences and tokens
in the converter, with support for both the original MPDT properties and the
converted Universal Dependencies properties.
"""
import re
from collections import defaultdict
from typing import Dict, List, Tuple, Optional
from utils.constants import feats_dict, MULTIWORD_EXPRESSIONS as MWE


class Sentence:
    """
    Class representing a sentence as a collection of tokens.

    A Sentence holds a list of Token objects and provides methods for accessing
    and manipulating the sentence structure, including finding the root token,
    accessing the sentence text, and managing sentence-level metadata.
    """

    def __init__(self, tokens: List['Token']) -> None:
        """
        Initialize a Sentence object.

        :param List[Token] tokens: List of Token objects that make up the sentence
        """
        self.tokens: List['Token'] = tokens
        self.dict_by_id: Dict[str, 'Token'] = {token.id: token for token in tokens}
        self.metadata = defaultdict(str)

        for token in tokens:
            token.sentence = self

    def get_root(self) -> Optional['Token']:
        """
        Returns the root token of the sentence.

        The root token is defined as the token whose gov_id is '0'.

        :return: The root Token object, or None if no root is found
        :rtype: Token | None
        """
        for token in self.tokens:
            if token.gov_id == '0':
                return token
        return None

    @property
    def text(self) -> str:
        """
        Returns the text of the sentence.

        If 'text' is available in the metadata, returns that value.
        Otherwise, returns the tokens joined by spaces.

        :return: The text of the sentence
        :rtype: str
        """
        if 'text' in self.metadata:
            return self.metadata['text']
        return " ".join(token.form for token in self.tokens)

    @property
    def meta(self) -> Dict[str, str]:
        """
        Returns the metadata of the sentence.

        :return: Dictionary of metadata for the sentence
        """
        return self.metadata

    @meta.setter
    def meta(self, value: Dict[str, str]) -> None:
        """
        Sets the metadata of the sentence.

        :param Dict[str, str] value: Dictionary of metadata to set
        """
        self.metadata.update(value)

    def write_meta(self, out) -> None:
        """
        Writes the metadata of the sentence to the given output stream.

        Each metadata key-value pair is written as a line in the format:

        \# key = value

        :param out: Output stream to write to
        """
        for key, value in self.meta.items():
            out.write(f"# {key} = {value}\n")

    def to_string(self, form='mpdt') -> str:
        """
        Returns a string representation of the sentence.

        The string consists of all tokens in the sentence, each on its own line.

        :return: String representation of the sentence
        :rtype: str
        """
        return "\n".join(token.to_string(form) for token in self.tokens)


class Token:
    """
    Class representing a token in a sentence.

    Each Token object stores both the original MPDT information and
    the converted UD information for a single token.
    """

    def __init__(self, line: str) -> None:
        """
        Initialize a Token object.

        :param str line: Line from the input file representing the token
        """
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
            self.data['eud'] = defaultdict(str)
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
            self.data['gov_id'] = '0'
            self.data['ugov_id'] = None
            self.data['gov'] = None
            self.data['ugov'] = None
            self.data['dep_label'] = '_'
            self.data['udep_label'] = '_'
            self.data['eud'] = defaultdict(str)
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
        """
        Returns the lemma of the token.

        :return: The lemmatized form of the token
        :rtype: str
        """
        return self.data['lemma']

    @lemma.setter
    def lemma(self, value: str) -> None:
        """
        Sets the lemma of the token.

        :param value: The lemmatized form to set
        """
        self.data['lemma'] = value

    @property
    def pos(self) -> str:
        """
        Returns the part of speech (POS) tag of the token in MPDT format.

        :return: The POS tag in MPDT format
        :rtype: str
        """
        return self.data['pos']

    @pos.setter
    def pos(self, value: str) -> None:
        """
        Sets the part of speech (POS) tag of the token in MPDT format.

        :param value: The POS tag in MPDT format to set
        """
        self.data['pos'] = value

    @property
    def pos_feats(self) -> str:
        """
        Returns the token's POS tag with its features in MPDT format.

        For example: "subst:sg:nom:m"

        :return: The POS tag with features
        :rtype: str
        """
        return self.data['pos_feats']

    @pos_feats.setter
    def pos_feats(self, value: str) -> None:
        """
        Sets the token's POS tag with its features in MPDT format.

        :param str value: The POS tag with features to set
        """
        self.data['pos_feats'] = value

    @property
    def feats(self) -> Dict[str, str]:
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
    def eud(self) -> Dict[str, str]:
        """Returns the enhanced dependencies of the token."""
        return self.data['eud']

    @eud.setter
    def eud(self, value: Dict[str, str]) -> None:
        """Updates the eud of the token."""
        self.data['eud'].update(value)

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
    def umisc(self) -> Dict[str, str]:
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
    def ufeats(self) -> Dict[str, str]:
        """Returns the ufeats of the token."""
        return self.data['ufeats']

    @ufeats.setter
    def ufeats(self, value: Dict[str, str]) -> None:
        """Updates the ufeats of the token."""
        self.data['ufeats'].update(value)

    @property
    def udep_label(self) -> str:
        """Returns the udep_label of the token."""
        return self.data['udep_label']

    @udep_label.setter
    def udep_label(self, value: Dict[str, str]) -> None:
        """Sets the udep_label of the token."""
        self.data['udep_label'] = value

    def to_string(self, form='mpdt') -> str:
        """
        Returns the Token as a line in CoNLL format or in UD CONLL-U format.
        Columns: ID, FORM, LEMMA, (U)POS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC.
        For FEATS, if no features are present, outputs '_'. DEPS is set to '_'.
        """
        if form == 'mpdt':
            upos_str = self.data['pos']
            feats_str = self.data['feats_raw']
            sent_str = self.data['sent_id']
            misc_str = self.data['misc']
        elif form == 'ud-tags-only':
            upos_str = self.data['upos']
            feats_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['ufeats'].items())]) if self.data['ufeats'] else '_'
            sent_str = '_'
            misc_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['umisc'].items())]) if self.data['umisc'] else '_'
        elif form == 'ud':
            upos_str = self.data['upos']
            feats_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['ufeats'].items())]) if self.data['ufeats'] else '_'
            sent_str = '_'
            misc_str = '|'.join([f'{k}={v}' for k, v in sorted(self.data['umisc'].items())]) if self.data['umisc'] else '_'
        else:
            raise ValueError(f"Invalid form parameters: {form}")

        return "\t".join([
            str(self.data['id']),
            self.data['form'],
            self.data['lemma'],
            upos_str,
            self.data['pos_feats'],
            feats_str,
            str(self.data['gov_id']),
            self.data['dep_label'],
            sent_str,
            misc_str
        ])

    @property
    def gov(self) -> Optional['Token']:
        """Returns the governor Token, or None if it's the root or something is missing."""
        if self.sentence is None:
            return None
        if self.gov_id == '0':
            return None
        return self.sentence.dict_by_id.get(self.gov_id)

    @property
    def ugov(self) -> Optional['Token']:
        """Returns the governor Token, or None if it's the root or something is missing."""
        if self.sentence is None:
            return None
        if self.ugov_id == '0':
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
    def prev(self) -> Optional['Token']:
        """Returns the previous token in the sentence."""
        if self.sentence is None:
            return None
        return self.sentence.dict_by_id.get(str(int(self.id) - 1), None)

    @property
    def next(self) -> Optional['Token']:
        """Returns the next token in the sentence."""
        if self.sentence is None:
            return None
        return self.sentence.dict_by_id.get(str(int(self.id) + 1), None)

    def children_with_label(self, label: str) -> List['Token']:
        """
        Returns a list of children of the token with the given dependency label.

        :param str label: The dependency label to look for
        :return: A list of children with the given label
        :rtype: List[Token]
        """
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if n.dep_label == label
        ]

    def children_with_ud_label(self, label: str) -> List['Token']:
        """Returns a list of children of the token with the given dependency label in UD format."""
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if n.udep_label == label
        ]

    def children_with_re_label(self, label: str) -> List['Token']:
        """Returns a list of children of the token with the given dependency label in regex format."""
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if re.search(label, n.dep_label)
        ]

    def children_with_lemma(self, lemma: str) -> List['Token']:
        """Returns a list of children of the token with the given lemma."""
        if self.sentence is None:
            return []
        return [
            n for n in self.children
            if n.lemma == lemma
        ]

    def super_gov_via_label(self, label: str) -> Optional[Tuple['Token', 'Token']]:
        """
        Recursively finds a governing token via a specific dependency path.

        This method looks for the first token in the upward dependency path
        that is connected via the specified label but whose governor is not
        connected via the same label.

        :param str label: The dependency label to follow in the recursion
        :return: The found governor Token, or None if not found
        :rtype: Token | None
        """
        if self.sentence is None:
            return None
        if self.dep_label == label:
            if self.gov.dep_label != label:
                return self.gov, self
            else:
                return self.gov.super_gov_via_label(label)
        return None

    def super_child_with_label_via_label(self, target_label: str, label: str) -> Optional['Token']:
        """
        Recursively finds a child token with a specific label following a path.

        This method first looks among direct children for one with the target label.
        If none is found, it recursively searches through the children connected
        via the specified label.

        :param str target_label: The dependency label to look for in children
        :param str label: The dependency label to follow in the recursive search
        :return: The found child Token, or None if not found
        :rtype: Token | None
        """
        if self.sentence is None:
            return None
        if self.dep_label == label:
            for child in self.children:
                if child.dep_label == target_label:
                    return child
                else:
                    return child.super_child_with_label_via_label(target_label, label)
        return None
