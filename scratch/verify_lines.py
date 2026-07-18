# -*- coding: utf-8 -*-
with open("d:/git_repo/TKprof_book/books/odyssey/chapters/ch_22_en.txt", "r", encoding="utf-8") as f:
    en_lines = f.readlines()

with open("d:/git_repo/TKprof_book/books/odyssey/chapters/ch_22_ko_proposal.txt", "r", encoding="utf-8") as f:
    ko_lines = f.readlines()

print(f"EN lines: {len(en_lines)}")
print(f"KO lines: {len(ko_lines)}")

# Strip newlines for comparison
en_clean = [l.strip() for l in en_lines]
ko_clean = [l.strip() for l in ko_lines]

mismatches = []
for i in range(max(len(en_clean), len(ko_clean))):
    en_val = en_clean[i] if i < len(en_clean) else None
    ko_val = ko_clean[i] if i < len(ko_clean) else None
    
    # Check empty line mismatch
    en_is_empty = not en_val
    ko_is_empty = not ko_val if ko_val is not None else True
    
    if en_is_empty != ko_is_empty:
        mismatches.append((i+1, en_val, ko_val))

if mismatches:
    print("Mismatches found (line numbers 1-indexed):")
    for line_num, en_v, ko_v in mismatches:
        print(f"Line {line_num}:")
        print(f"  EN: {repr(en_v)}")
        print(f"  KO: {repr(ko_v)}")
else:
    print("Line counts and empty/non-empty patterns match perfectly!")
