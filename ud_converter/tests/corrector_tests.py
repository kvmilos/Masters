"""
Pytest-style tests for the corrector module.

This module contains validation tests for CoNLL files to ensure they follow 
the expected format and constraints. The tests verify:
  - The POS (column 4) is a known POS tag
  - Each feature in the FEATS column (column 6) is in feats_dict
  - The features listed in the POS_FEATS column (column 5, after the first element)
    (via feats_dict mapping) are allowed for that POS
"""
from typing import List
from utils.constants import feats_dict, feats_of_pos


def test_pos(lines: List[str]) -> None:
    """
    Validates that every POS tag in the input is in the allowed set.
    
    :param lines: List of CoNLL format lines to validate
    :raises AssertionError: for invalid POS tags
    """
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t')
        pos = fields[3]
        assert pos in feats_of_pos, f"POS {pos} is not in the allowed list: {list(feats_of_pos.keys())}"
    print("test_pos passed")

def test_feats(lines: List[str]) -> None:
    """
    Validates that every feature in the FEATS column is in the allowed set.
    
    :param lines: List of CoNLL format lines to validate
    :raises AssertionError: for invalid features
    """
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t')
        feats_field = fields[5]
        if feats_field != "_" and feats_field:
            feats_list = feats_field.split("|")
            if feats_list:
                for feat in feats_list:
                    assert feat in feats_dict, f"Feature {feat} is not in feats_dict."
    print("test_feats passed")

def test_feats_pos_combination(lines: List[str]) -> None:
    """
    Validates that features from POS_FEATS are allowed for the given POS.
    
    Ensures that for each line, the features from the POS_FEATS field (field 5, 
    after the POS) mapped via feats_dict are allowed for that specific POS tag
    according to the feats_of_pos dictionary.
    
    :param lines: List of CoNLL format lines to validate
    :raises AssertionError: for invalid feature-POS combinations
    """
    for line in lines:
        if not line.strip():
            continue
        fields = line.split('\t')
        pos = fields[3]
        pos_feats_field = fields[4]
        parts = pos_feats_field.split(":")
        if len(parts) > 1:
            feats_from_pos_feats = parts[1:]
            for feat in feats_from_pos_feats:
                mapped = feats_dict.get(feat)
                allowed = feats_of_pos.get(pos, [])
                assert mapped in allowed, f"Feature {feat} (mapped as {mapped}) is not allowed for POS {pos}."
    print("test_feats_pos_combination passed")
