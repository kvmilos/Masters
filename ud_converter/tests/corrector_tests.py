"""
Tests for corrector.py.
"""
from utils.pos_list import pos_list
from utils.feats_dict import feats_dict
from utils.possible_feats_based_on_pos import feats_of_pos

def test_pos(pos: str):
    """
    Tests if a POS is in pos_list.
    """
    if pos not in pos_list:
        print(f"POS {pos} is not in the list of possible POSs.")


def test_feats(feats: list[str]):
    """
    Tests if all the feats are in feats_dict.
    """
    for feat in feats:
        if feat not in feats_dict:
            print(f"FEAT {feat} is not in the list of possible feats.")


def test_feats_pos_combination(pos: str, feats: list[str]):
    """
    Tests if all the feats are in the list of possible feats for a given POS.
    """
    for feat in feats:
        if feats_dict[feat] not in feats_of_pos[pos]:
            print(f"FEAT {feat} is not in the list of possible feats for POS {pos}.")
