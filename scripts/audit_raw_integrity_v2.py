import json
import glob
import os
import re
import difflib

# We will match per file to avoid difflib blowing up on 600k char strings

# Load all source text
with open('c:/git_repo/TKprof_book/books/two_cities/raw_source.txt', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = 0
for i, line in enumerate(lines):
    if line.startswith("Book the First--Recalled to Life") and i > 150:
        start_idx = i
        break
end_idx = len(lines)
for i, line in enumerate(lines):
    if line.startswith("*** END OF THE PROJECT GUTENBERG"):
        end_idx = i
        break
source_full = ' '.join([line.strip() for line in lines[start_idx:end_idx]])

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

source_norm = normalize(source_full)

# Load all JSON text
files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))

json_text_full = ""
for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except:
        continue
    for block in data:
        if isinstance(block, dict):
            json_text_full += block.get('raw', '') + " "

json_norm = normalize(json_text_full)

print(f"JSON chars: {len(json_norm)}, Source chars: {len(source_norm)}")

import sys
sys.setrecursionlimit(20000)

matcher = difflib.SequenceMatcher(None, source_norm, json_norm)
opcodes = matcher.get_opcodes()

omissions = []
additions = []

for tag, i1, i2, j1, j2 in opcodes:
    if tag in ('delete', 'replace'):
        missing = source_norm[i1:i2]
        if len(missing) > 5:  # Ignore tiny punctuation differences
            context = source_norm[max(0, i1-40):i1] + " >>>" + missing + "<<< " + source_norm[i2:min(len(source_norm), i2+40)]
            omissions.append(context)
    if tag in ('insert', 'replace'):
        added = json_norm[j1:j2]
        if len(added) > 5:
            context = json_norm[max(0, j1-40):j1] + " >>>" + added + "<<< " + json_norm[j2:min(len(json_norm), j2+40)]
            additions.append(context)

with open('c:/git_repo/TKprof_book/raw_integrity_report_v2.md', 'w', encoding='utf-8') as out:
    out.write(f"# Integrity Report V2\n\nOmissions: {len(omissions)}\nAdditions: {len(additions)}\n\n")
    out.write("## Omissions (In Source, Missing in JSON)\n")
    for o in omissions:
        out.write(f"- {o}\n")
    out.write("\n## Additions (In JSON, Missing in Source)\n")
    for a in additions:
        out.write(f"- {a}\n")

print("Done v2")
