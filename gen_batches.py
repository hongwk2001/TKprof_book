import json

with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_12.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

missing = [item for item in data if not item['en'] or not item['ko']]
batch_size = 10
batches = [missing[i:i + batch_size] for i in range(0, len(missing), batch_size)]

print(f"Total missing: {len(missing)}")
print(f"Total batches: {len(batches)}")

import sys
import json
subagents = []
for i, b in enumerate(batches):
    prompt = "Please translate the following blocks to English ('en') and Korean ('ko'). Return ONLY valid JSON format containing a list of objects with 'tag', 'en', and 'ko'.\n\n"
    for item in b:
        prompt += f"Tag: {item['tag']}\nRaw: {item['raw']}\n\n"
    
    subagents.append({
        "TypeName": "SegmentTranslator",
        "Role": "Translator",
        "Prompt": prompt
    })

with open('subagents.json', 'w', encoding='utf-8') as f:
    json.dump(subagents, f, indent=2)
