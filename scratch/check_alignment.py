import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("d:/git_repo/TKprof_book/books/odyssey/chapters/ch_12_en.txt", "r", encoding="utf-8") as f:
    en_lines = f.readlines()

with open("d:/git_repo/TKprof_book/books/odyssey/chapters/ch_12_ko_proposal.txt", "r", encoding="utf-8") as f:
    ko_lines = f.readlines()

print(f"EN lines: {len(en_lines)}, KO lines: {len(ko_lines)}")

max_len = max(len(en_lines), len(ko_lines))
for i in range(max_len):
    en_val = en_lines[i].strip() if i < len(en_lines) else "[[EOF]]"
    ko_val = ko_lines[i].strip() if i < len(ko_lines) else "[[EOF]]"
    
    en_empty = len(en_val) == 0
    ko_empty = len(ko_val) == 0
    
    if en_empty != ko_empty:
        print(f"Mismatch at line {i+1}:")
        print(f"  EN empty: {en_empty} | content: {en_val[:30]}")
        print(f"  KO empty: {ko_empty} | content: {ko_val[:30]}")
