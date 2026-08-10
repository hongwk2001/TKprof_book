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

def get_words(text, n=3):
    words = text.split()
    if len(words) <= 2*n:
        return text
    return " ".join(words[:n]) + " ... " + " ".join(words[-n:])

out = []
for i, item in enumerate(data):
    out.append(f"\n=== Task {i} (Index {item['paragraph_index']}) ===")
    en_chunks = item['english_chunks']
    ko_text = item['korean_original']
    ko_sents = split_sentences(ko_text)
    
    out.append("ENGLISH CHUNKS:")
    for j, chunk in enumerate(en_chunks):
        out.append(f"  Chunk {j}: {get_words(chunk, 5)}")
        
    out.append("KOREAN SENTENCES:")
    for k, sent in enumerate(ko_sents):
        out.append(f"  [{k}] {get_words(sent, 5)}")

with open('C:/git_repo/TKprof_book/summary.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(out))
