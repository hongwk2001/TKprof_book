import json, re

with open('c:/git_repo/TKprof_book/books/dracula/chapters/ch21_en.txt', 'r', encoding='utf-8') as f:
    en_text = f.read()

en_paragraphs = re.findall(r'\[P\d{3}\](.*?)(?=\n\n\[P|\Z)', en_text, re.DOTALL)
en_lengths = [len(p.split()) for p in en_paragraphs[14:25]]

with open('c:/git_repo/TKprof_book/ko_clean_lines.json', 'r', encoding='utf-8') as f:
    lines = json.load(f)

combined = ' '.join(lines[14:25])
sentences = re.split(r'(?<=[.!?\u201d\"])\s+', combined)
sentences = [s.strip() for s in sentences if s.strip()]

total_en = sum(en_lengths)
total_sentences = len(sentences)

chunks = []
idx = 0
for i, L in enumerate(en_lengths):
    if i == 10:
        chunks.append(' '.join(sentences[idx:]))
        break
    count = int(round(L / total_en * total_sentences))
    if count == 0: count = 1
    chunks.append(' '.join(sentences[idx:idx+count]))
    idx += count

lines[14:25] = chunks

clean_lines = [re.sub(r'^\[P\d{3}\]\s*', '', l).strip() for l in lines]

with open('c:/git_repo/TKprof_book/books/dracula/chapters/aligned_ko_ch21.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(clean_lines))

print('Total paragraphs:', len(clean_lines))
