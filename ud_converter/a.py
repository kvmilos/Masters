import re
from collections import Counter
import pandas as pd

full_log_text = """
[Line 8976 Sent 319 Node 17]: [L3 Syntax too-many-subjects] Multiple subjects [2, 14] ('linia liniia', 'linie liniie') not subtyped as ':outer'. Outer subjects are allowed if a clause acts as the predicate of another clause.
[Line 9278 Sent 330 Node 2]: [L3 Syntax right-to-left-appos] Parent of relation 'appos' must precede the child in the word order.
[Line 9281 Sent 330 Node 5]: [L3 Syntax right-to-left-appos] Parent of relation 'appos' must precede the child in the word order.
[Line 13460 Sent 484]: [L3 Syntax rel-upos-nummod] 'nummod' should be 'NUM' but it is 'ADP' ('36 36')
[Line 13962 Sent 501]: [L3 Syntax rel-upos-det] 'det' should be 'DET' or 'PRON' but it is 'NUM' ('300 300')
[Line 17535 Sent 633 Node 8]: [L3 Syntax too-many-subjects] Multiple subjects [3, 7] ('ty ty', 'on on') not subtyped as ':outer'.
[Line 17743 Sent 639 Node 8]: [L3 Syntax right-to-left-fixed] Parent of relation 'fixed' must precede the child in the word order.
[Line 18381 Sent 661 Node 5]: [L3 Syntax leaf-cc] 'cc' not expected to have children (5:bądź:cc --> 6:to:advmod)
[Line 19219 Sent 689]: [L3 Syntax rel-upos-fixed] 'fixed' should not be used for proper nouns ('Jego Je^o^').
[Line 20382 Sent 727 Node 7]: [L3 Syntax right-to-left-appos] Parent of relation 'appos' must precede the child in the word order.
[Line 21246 Sent 755]: [L2 Syntax head-self-loop] HEAD == ID for 29
[Line 23397 Sent 831 Node 3]: [L3 Syntax leaf-aux-cop] 'cop' not expected to have children (3:jest:cop --> 2:reguła:nsubj)
[Line 27742 Sent 983 Node 6]: [L3 Syntax too-many-subjects] Multiple subjects [1, 4] ('Kto Kto', 'kto kto') not subtyped as ':outer'.
[Line 28171 Sent 999 Node 9]: [L3 Syntax leaf-cc] 'cc' not expected to have children (9:czyli:cc --> 10:to:advmod)
[Line 34103 Sent 1202]: [L2 Syntax head-self-loop] HEAD == ID for 11
[Line 34175 Sent 1205 Node 2]: [L3 Syntax leaf-cc] 'cc' not expected to have children (2:tylko:cc --> 3:ć:advmod)
[Line 34720 Sent 1222 Node 18]: [L3 Syntax too-many-subjects] Multiple subjects [2, 14] ('sposób sposob', 'kręciły kręciły') not subtyped as ':outer'.
[Line 46811 Sent 1630 Node 36]: [L3 Syntax right-to-left-fixed] Parent of relation 'fixed' must precede the child in the word order.
[Line 48764 Sent 1702 Node 15]: [L3 Syntax leaf-det] 'det' not expected to have children (15:tych:det --> 18:lubią:acl)
"""
full_error_types = re.findall(r'\[L3 (Syntax|Warning) ([\w\-]+)\]', full_log_text)

# Count occurrences
full_counter = Counter(f"{typ} {name}" for typ, name in full_error_types)

# Convert to sorted list of tuples
sorted_full_errors = sorted(full_counter.items(), key=lambda x: x[1], reverse=True)

# Create DataFrame
full_df = pd.DataFrame(sorted_full_errors, columns=["Error Type", "Count"])

# Display full data to user
print(full_df)
