import re
from collections import Counter
import pandas as pd

FULL_LOG_TEXT = """
"""
full_error_types = re.findall(r'\[L3 (Syntax|Warning) ([\w\-]+)\]', FULL_LOG_TEXT)

# Count occurrences
full_counter = Counter(f"{typ} {name}" for typ, name in full_error_types)

# Convert to sorted list of tuples
sorted_full_errors = sorted(full_counter.items(), key=lambda x: x[1], reverse=True)

# Create DataFrame
full_df = pd.DataFrame(sorted_full_errors, columns=["Error Type", "Count"])

# Display full data to user
print(full_df)
