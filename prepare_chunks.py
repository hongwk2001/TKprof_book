import os
import re
import json

def split_english_paragraph(text, max_len=600):
    # Regex to match sentence endings followed by space or newline
    # We want to keep the punctuation with the sentence.
    pattern = r'(?<=[.?!])(?=[\'\"]?\s+)'
    sentences = re.split(pattern, text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = []
    current_len = 0
    
    for s in sentences:
        if current_len + len(s) > max_len and current_len > 0:
            chunks.append(' '.join(current_chunk))
            current_chunk = [s]
            current_len = len(s)
        else:
            current_chunk.append(s)
            current_len += len(s)
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

os.makedirs('books/dracula/chunk_tasks', exist_ok=True)

total_tasks = 0

for i in range(1, 28):
    ch = f'ch{i:02d}'
    en_file = f'books/dracula/chapters/{ch}_en.txt'
    ko_file = f'books/dracula/chapters/{ch}_ko.txt'
    
    if not os.path.exists(en_file) or not os.path.exists(ko_file):
        continue
        
    with open(en_file, 'r', encoding='utf-8') as f:
        en_paras = [p for p in f.read().split('\n\n') if p.strip()]
        
    with open(ko_file, 'r', encoding='utf-8') as f:
        ko_paras = [p for p in f.read().split('\n\n') if p.strip()]
        
    if len(en_paras) != len(ko_paras):
        print(f"ERROR: {ch} parity mismatch. EN: {len(en_paras)}, KO: {len(ko_paras)}")
        continue
        
    chapter_tasks = []
    
    for p_idx, (en_p, ko_p) in enumerate(zip(en_paras, ko_paras)):
        if len(en_p) > 800:
            en_chunks = split_english_paragraph(en_p, max_len=600)
            if len(en_chunks) > 1:
                chapter_tasks.append({
                    "paragraph_index": p_idx,
                    "english_chunks": en_chunks,
                    "korean_original": ko_p
                })
                total_tasks += 1
                
    if chapter_tasks:
        with open(f'books/dracula/chunk_tasks/{ch}_tasks.json', 'w', encoding='utf-8') as f:
            json.dump(chapter_tasks, f, ensure_ascii=False, indent=2)

print(f"Generated tasks for {total_tasks} paragraphs.")
