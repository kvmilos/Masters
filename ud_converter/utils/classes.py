"""
Module for the Sentence and Token classes.
"""
from collections import defaultdict
from utils.feats_dict import feats_dict

class Sentence:
    """
    A Sentence holds a list of Node objects.
    It provides a get_root method returning the Node whose gov_id == "0".
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.dict_by_id = {token.id: token for token in tokens}

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
    def text(self):
        """Returns the text of the sentence."""
        return " ".join([token.form for token in self.tokens])

    def __str__(self):
        """Returns the sentence as its tokens joined by newline."""
        return "\n".join(str(token) for token in self.tokens)


class Token:
    """
    A token has its properties:
    id, form, lemma, pos, pos_feats, feats, gov_id, dep_label, sent_id, misc
    """
    def __init__(self, line):
        columns = line.split("\t")
        self.data = {}
        self.data['id'] = columns[0]
        self.data['form'] = columns[1]
        self.data['lemma'] = columns[2]
        self.data['pos'] = columns[3]
        self.data['pos_feats'] = columns[4]
        self.data['feats_raw'] = columns[5]
        if self.data['feats_raw'] != "_":
            self.data['feats'] = {feats_dict[feat]: feat for feat in self.data['feats_raw'].split("|")}
        else:
            self.data['feats'] = {}
        self.data['gov_id'] = columns[6]
        self.data['gov'] = None
        self.data['dep_label'] = columns[7]
        self.data['sent_id'] = columns[8]
        self.data['misc'] = {'Translit': columns[9]}
        self.sentence = None
        self.data['upos'] = None
        self.data['ufeats'] = defaultdict(str)
        self.data['udep_label'] = None

    @property
    def id(self):
        """Returns the id of the token."""
        return self.data['id']

    @id.setter
    def id(self, value):
        """Sets the id of the token."""
        self.data['id'] = value

    @property
    def form(self):
        """Returns the form of the token."""
        return self.data['form']

    @form.setter
    def form(self, value):
        """Sets the form of the token."""
        self.data['form'] = value

    @property
    def lemma(self):
        """Returns the lemma of the token."""
        return self.data['lemma']

    @lemma.setter
    def lemma(self, value):
        """Sets the lemma of the token."""
        self.data['lemma'] = value

    @property
    def pos(self):
        """Returns the pos of the token."""
        return self.data['pos']

    @pos.setter
    def pos(self, value):
        """Sets the pos of the token."""
        self.data['pos'] = value

    @property
    def pos_feats(self):
        """Returns the token's pos with its features."""
        return self.data['pos_feats']

    @pos_feats.setter
    def pos_feats(self, value):
        """Sets the token's pos with its features."""
        self.data['pos_feats'] = value

    @property
    def feats(self):
        """Returns a dictionary of feats for the token."""
        return self.data['feats']

    @feats.setter
    def feats(self, value):
        """Sets the dictionary of feats for the token."""
        self.data['feats'] = value
        self.data['feats_raw'] = "|".join(value.values())

    @property
    def gov_id(self):
        """Returns the id of the governor of the token."""
        return self.data['gov_id']

    @gov_id.setter
    def gov_id(self, value):
        """Sets the id of the governor of the token."""
        self.data['gov_id'] = value

    @property
    def dep_label(self):
        """Returns the dependency label of the token."""
        return self.data['dep_label']

    @dep_label.setter
    def dep_label(self, value):
        """Sets the dependency label of the token."""
        self.data['dep_label'] = value

    @property
    def sent_id(self):
        """Returns the id of the sentence of the token."""
        return self.data['sent_id']

    @sent_id.setter
    def sent_id(self, value):
        """Sets the id of the sentence of the token."""
        self.data['sent_id'] = value

    @property
    def misc(self):
        """Returns the misc of the token."""
        return self.data['misc']

    @misc.setter
    def misc(self, value):
        """Sets the misc of the token."""
        self.data['misc'] = value

    @property
    def feats_raw(self):
        """Returns the raw feats of the token."""
        return self.data['feats_raw']

    @feats_raw.setter
    def feats_raw(self, value):
        """Sets the raw feats of the token."""
        self.data['feats_raw'] = value
        self.data['feats'] = {feats_dict[feat]: feat for feat in value.split("|")}

    @property
    def upos(self):
        """Returns the upos of the token."""
        return self.data['upos']

    @upos.setter
    def upos(self, value):
        """Sets the upos of the token."""
        self.data['upos'] = value

    @property
    def ufeats(self):
        """Returns the ufeats of the token."""
        return self.data['ufeats']

    @ufeats.setter
    def ufeats(self, value):
        """Updates the ufeats of the token."""
        self.data['ufeats'].update(value)

    @property
    def udep_label(self):
        """Returns the udep_label of the token."""
        return self.data['udep_label']

    @udep_label.setter
    def udep_label(self, value):
        """Sets the udep_label of the token."""
        self.data['udep_label'] = value

    def __str__(self):
        """
        Returns the Token as a line in UD CONLL-U format.
        Columns: ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC.
        For FEATS, if no features are present, outputs '_'. DEPS is set to '_'.
        """
        feats_str = "|".join(self.data['feats'].values()) if self.data['feats'] else "_"
        misc_str = self.data['misc'].get("Translit", "_") if isinstance(self.data['misc'], dict) else str(self.data['misc'])
        return "\t".join([
            self.data['id'],
            self.data['form'],
            self.data['lemma'],
            self.data['upos'] if self.data['upos'] else self.data['pos'],
            self.data['pos_feats'],
            feats_str,
            self.data['gov_id'],
            self.data['dep_label'],
            "_",
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
    def children(self):
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
        return self.sentence.dict_by_id.get(self.id - 1, None)

    @property
    def next(self):
        """Returns the next token in the sentence."""
        if self.sentence is None:
            return None
        return self.sentence.dict_by_id.get(self.id + 1, None)
