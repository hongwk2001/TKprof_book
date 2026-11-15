import json
import glob
import os
import re
import difflib

# 1. Reconstruct text from JSONs
files = sorted(glob.glob('c:/git_repo/TKprof_book/books/two_cities/json/book*_ch_*.json'))

json_text = []
for f in files:
    try:
        data = json.load(open(f, encoding='utf-8'))
    except Exception as e:
        print(f"Error reading {f}: {e}")
        continue
    
    for block in data:
        if isinstance(block, dict):
            # We skip headers because the source text has different formatting for headers
            if block.get('is_header'):
                continue
            raw = block.get('raw', '')
            json_text.append(raw)

json_full = ' '.join(json_text)

# 2. Extract text from raw_source.txt
with open('c:/git_repo/TKprof_book/books/two_cities/raw_source.txt', encoding='utf-8') as f:
    lines = f.readlines()

# The actual text starts around line 199 ("Book the First")
start_idx = 0
for i, line in enumerate(lines):
    if line.startswith("Book the First--Recalled to Life") and i > 150:
        start_idx = i
        break

# The text ends before "*** END OF THE PROJECT GUTENBERG EBOOK"
end_idx = len(lines)
for i, line in enumerate(lines):
    if line.startswith("*** END OF THE PROJECT GUTENBERG"):
        end_idx = i
        break

source_full = ' '.join([line.strip() for line in lines[start_idx:end_idx]])

# 3. Normalize both texts (remove all non-alphanumeric chars)
def normalize(text):
    # Convert to lowercase and keep only alphanumeric chars
    return re.sub(r'[^a-z0-9]', '', text.lower())

json_norm = normalize(json_full)
source_norm = normalize(source_full)

print(f"JSON normalized length: {len(json_norm)}")
print(f"Source normalized length: {len(source_norm)}")

# 4. Diffing
if json_norm == source_norm:
    print("SUCCESS: 100% MATCH! No omissions or duplications.")
    with open('c:/git_repo/TKprof_book/raw_integrity_report.md', 'w', encoding='utf-8') as out:
        out.write("# Raw Text Integrity Report\n\n**SUCCESS: 100% MATCH!**\nNo omissions or duplications were found. The JSON files perfectly mirror the original source text.")
else:
    print("MISMATCH DETECTED. Generating detailed report...")
    
    matcher = difflib.SequenceMatcher(None, source_norm, json_norm)
    opcodes = matcher.get_opcodes()
    
    with open('c:/git_repo/TKprof_book/raw_integrity_report.md', 'w', encoding='utf-8') as out:
        out.write("# Raw Text Integrity Report\n\n**MISMATCH DETECTED.**\n\n")
        out.write("## Omissions (In source, but missing in JSON)\n")
        
        has_omissions = False
        for tag, i1, i2, j1, j2 in opcodes:
            if tag in ('delete', 'replace'):
                has_omissions = True
                missing_str = source_norm[i1:i2]
                context_before = source_norm[max(0, i1-30):i1]
                context_after = source_norm[i2:min(len(source_norm), i2+30)]
                out.write(f"- At source offset {i1}:\n")
                out.write(f"  Context: `...{context_before}` **[MISSING: {missing_str}]** `{context_after}...`\n\n")
        
        if not has_omissions:
            out.write("None found.\n\n")
            
        out.write("## Duplications / Additions (In JSON, but not in source)\n")
        
        has_dupes = False
        for tag, i1, i2, j1, j2 in opcodes:
            if tag in ('insert', 'replace'):
                has_dupes = True
                added_str = json_norm[j1:j2]
                context_before = json_norm[max(0, j1-30):j1]
                context_after = json_norm[j2:min(len(json_norm), j2+30)]
                out.write(f"- At JSON offset {j1}:\n")
                out.write(f"  Context: `...{context_before}` **[ADDED: {added_str}]** `{context_after}...`\n\n")
                
        if not has_dupes:
            out.write("None found.\n")
    
    print("Report written to raw_integrity_report.md")
