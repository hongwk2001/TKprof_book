import json
import re

with open('C:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch19_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def split_sentences(text):
    sents = re.split(r'([.?!]+\"?\s+)', text.strip())
    result = []
    current = ""
    for i, part in enumerate(sents):
        if i % 2 == 0:
            current += part
        else:
            current += part
            result.append(current.strip())
            current = ""
    if current:
        result.append(current.strip())
    return [s for s in result if s]

out = []
for i, item in enumerate(data):
    out.append(f"=== Task {i} ===")
    for j, chunk in enumerate(item['english_chunks']):
        sents = split_sentences(chunk)
        if sents:
            out.append(f"Chunk {j} end: {sents[-1]}")
    ko_sents = split_sentences(item['korean_original'])
    for k, sent in enumerate(ko_sents):
        out.append(f"KO [{k}]: {sent}")

with open('C:/git_repo/TKprof_book/last_sents.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
