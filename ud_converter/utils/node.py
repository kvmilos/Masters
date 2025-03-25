"""
Module for the Node class.
"""
from utils.feats_dict import feats_dict

class Node:
    """
    Each node is a token + its specific properties.
    n_id, form, lemma, pos, pos_feats, feats, gov_id, dep_label, sent_id, misc
    """
    def __init__(self, line):
        columns = line.split("\t")
        self.data = {}
        self.data['n_id'] = columns[0]
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
        self.data['misc'] = columns[9]

    @property
    def id(self):
        """
        Returns the id of the node.
        """
        return self.data['n_id']

    @id.setter
    def id(self, value):
        """
        Sets the id of the node.
        """
        self.data['n_id'] = value

    @property
    def form(self):
        """
        Returns the form of the node.
        """
        return self.data['form']

    @form.setter
    def form(self, value):
        """
        Sets the form of the node.
        """
        self.data['form'] = value

    @property
    def lemma(self):
        """
        Returns the lemma of the node.
        """
        return self.data['lemma']

    @lemma.setter
    def lemma(self, value):
        """
        Sets the lemma of the node.
        """
        self.data['lemma'] = value

    @property
    def pos(self):
        """
        Returns the pos of the node.
        """
        return self.data['pos']

    @pos.setter
    def pos(self, value):
        """
        Sets the pos of the node.
        """
        self.data['pos'] = value

    @property
    def pos_feats(self):
        """
        Returns the node's pos with its features.
        """
        return self.data['pos_feats']

    @pos_feats.setter
    def pos_feats(self, value):
        """
        Sets the node's pos with its features.
        """
        self.data['pos_feats'] = value

    @property
    def feats(self):
        """
        Returns a dictionary of feats for the node.
        """
        return self.data['feats']

    @feats.setter
    def feats(self, value):
        """
        Sets the dictionary of feats for the node.
        """
        self.data['feats'] = value
        self.data['feats_raw'] = "|".join(value.values())

    @property
    def gov_id(self):
        """
        Returns the id of the governor of the node.
        """
        return self.data['gov_id']

    @gov_id.setter
    def gov_id(self, value):
        """
        Sets the id of the governor of the node.
        """
        self.data['gov_id'] = value

    @property
    def dep_label(self):
        """
        Returns the dependency label of the node.
        """
        return self.data['dep_label']

    @dep_label.setter
    def dep_label(self, value):
        """
        Sets the dependency label of the node.
        """
        self.data['dep_label'] = value

    @property
    def sent_id(self):
        """
        Returns the id of the sentence of the node.
        """
        return self.data['sent_id']

    @sent_id.setter
    def sent_id(self, value):
        """
        Sets the id of the sentence of the node.
        """
        self.data['sent_id'] = value

    @property
    def misc(self):
        """
        Returns the misc of the node.
        """
        return self.data['misc']

    @misc.setter
    def misc(self, value):
        """
        Sets the misc of the node.
        """
        self.data['misc'] = value

    @property
    def feats_raw(self):
        """
        Returns the raw feats of the node.
        """
        return self.data['feats_raw']

    @feats_raw.setter
    def feats_raw(self, value):
        """
        Sets the raw feats of the node.
        """
        self.data['feats_raw'] = value
        self.data['feats'] = {feats_dict[feat]: feat for feat in value.split("|")}

    def __str__(self):
        """
        Returns the Node as a line in CONLL format (MPDT, not UD).
        """
        return "\t".join([
        self.data['n_id'],
        self.data['form'],
        self.data['lemma'],
        self.data['pos'],
        self.data['pos_feats'],
        self.data['feats_raw'],
        self.data['gov_id'],
        self.data['dep_label'],
        self.data['sent_id'],
        self.data['misc']
    ])

    def ud_conll(self):
        """
        Returns the Node as a line in UD CONLL format.
        """
        ...
