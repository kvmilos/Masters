import re
from collections import Counter
import pandas as pd

#                           Error Type  Count
# 0       Morpho feature-value-unknown     14
# 1              Warning orphan-parent      9
# 2                  Warning fixed-gap      8
# 3  Morpho feature-upos-not-permitted      4

FULL_LOG_TEXT = """
[Line 10238 Sent 363 Node 2]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<363#2, skąd>, Node<363#4, inąd>] 'skąd * inąd'
[Line 12335 Sent 440]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 14323 Sent 515]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 16124 Sent 582]: [L4 Morpho feature-upos-not-permitted] Feature NumType is not permitted with UPOS ADV in language [pl].
[Line 24565 Sent 869]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 28476 Sent 1011]: [L4 Morpho feature-value-unknown] Value X is not documented for feature ExtPos in language [pl].
[Line 30671 Sent 1085 Node 34]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 31296 Sent 1105 Node 7]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 33216 Sent 1171 Node 4]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1171#4, tym>, Node<1171#6, samym>] 'tym * samym'
[Line 33321 Sent 1175 Node 7]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'nmod'.
[Line 34150 Sent 1204]: [L4 Morpho feature-value-unknown] Value VERB is not documented for feature ExtPos in language [pl].
[Line 34174 Sent 1205]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 36035 Sent 1265]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 36047 Sent 1265]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 36849 Sent 1289 Node 24]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 37644 Sent 1315]: [L4 Morpho feature-upos-not-permitted] Feature NumType is not permitted with UPOS ADV in language [pl].
[Line 39157 Sent 1366 Node 14]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'obl'.
[Line 39992 Sent 1397 Node 9]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1397#9, to>, Node<1397#11, samo>] 'to * samo'
[Line 40912 Sent 1429 Node 9]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1429#9, ten>, Node<1429#11, sam>] 'ten * sam'
[Line 44381 Sent 1545]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 46956 Sent 1635]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 47645 Sent 1659]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 47834 Sent 1666]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 47834 Sent 1666 Node 9]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1666#9, co>, Node<1666#12, za>] 'co * * za'
[Line 49606 Sent 1732 Node 7]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1732#7, ten>, Node<1732#9, sam>] 'ten * sam'
[Line 49778 Sent 1740 Node 18]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 49912 Sent 1744 Node 13]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 50469 Sent 1764 Node 3]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 50632 Sent 1770 Node 19]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1770#19, to>, Node<1770#21, samo>] 'to * samo'
[Line 50843 Sent 1777]: [L4 Morpho feature-upos-not-permitted] Feature NumType is not permitted with UPOS ADV in language [pl].
[Line 51754 Sent 1810 Node 28]: [L3 Warning orphan-parent] The parent of 'orphan' should normally be 'conj' but it is 'dep'.
[Line 54551 Sent 1908]: [L4 Morpho feature-value-unknown] Value NOUN is not documented for feature ExtPos in language [pl].
[Line 54551 Sent 1908 Node 8]: [L3 Warning fixed-gap] Gaps in fixed expression [Node<1908#8, kroć>, Node<1908#10, tysięcy>] 'kroć * tysięcy'
[Line 54763 Sent 1913]: [L4 Morpho feature-value-unknown] Value PART is not documented for feature ExtPos in language [pl].
[Line 56110 Sent 1959]: [L4 Morpho feature-upos-not-permitted] Feature NumType is not permitted with UPOS ADV in language [pl].
"""
full_error_types = re.findall(r'\[(L3|L4) (Syntax|Warning|Morpho) ([\w\-]+)\]', FULL_LOG_TEXT)

# Count occurrences
full_counter = Counter(f"{typ} {name}" for _, typ, name in full_error_types)

# Convert to sorted list of tuples
sorted_full_errors = sorted(full_counter.items(), key=lambda x: x[1], reverse=True)

# Create DataFrame
full_df = pd.DataFrame(sorted_full_errors, columns=["Error Type", "Count"])

# Display full data to user
print(full_df)
