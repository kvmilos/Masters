"""
Script to join two JSON files containing metadata for MPDT sentences.
"""
import json

with open('../data/meta/MPDT_1.json', encoding='utf-8') as f1:
    mpdt1 = json.load(f1)

with open('../data/meta/MPDT_2.json', encoding='utf-8') as f2:
    mpdt2 = json.load(f2)

max_id_mpdt1 = max(int(key) for key in mpdt1.keys())

combined_data = {}

for key, value in mpdt1.items():
    if isinstance(value, dict) and "sent_id" in value:
        value["sent_id"] = key
    combined_data[key] = value

for idx, (_, value) in enumerate(mpdt2.items(), 1):
    NEW_ID = str(max_id_mpdt1 + idx)
    if isinstance(value, dict) and "sent_id" in value:
        value["sent_id"] = NEW_ID
    combined_data[NEW_ID] = value

with open('../data/meta/MPDT_2000.json', 'w', encoding='utf-8') as f_out:
    json.dump(combined_data, f_out, indent=4, ensure_ascii=False)
