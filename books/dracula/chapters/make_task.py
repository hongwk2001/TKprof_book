import re
import json

en_file = r"C:\git_repo\TKprof_book\books\dracula\chapters\ch06_en.txt"
ko_file = r"C:\git_repo\TKprof_book\books\dracula\chapters\ch06_ko.txt"

with open(en_file, 'r', encoding='utf-8') as f:
    en_lines = f.read().split('\n\n')

en_paragraphs = [re.sub(r'\[P\d{3}\]\s*', '', p).strip() for p in en_lines if p.strip()]

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

ko_text = re.sub(r'\[P\d{3}\]', ' ', ko_text)
ko_text = re.sub(r'\s+', ' ', ko_text).strip()

out_obj = {
    "paragraph_index": "ch06",
    "english_chunks": en_paragraphs,
    "korean_original": ko_text
}

with open(r"C:\git_repo\TKprof_book\books\dracula\chapters\task.json", 'w', encoding='utf-8') as f:
    json.dump([out_obj], f, ensure_ascii=False, indent=2)

print(f"Created task.json with {len(en_paragraphs)} English paragraphs.")
print("Korean length:", len(ko_text))
