import json
import re

def proportional_split(english_chunks, korean_original):
    if len(english_chunks) == 1:
        return [korean_original]
    
    # Calculate ratios
    lengths = [len(c) for c in english_chunks]
    total_len = sum(lengths)
    ratios = [l / total_len for l in lengths]
    
    kor_len = len(korean_original)
    
    # Find all sentence boundaries
    boundaries = [0] + [m.end() for m in re.finditer(r'[.?!](?:\"|\')?\s+', korean_original)] + [kor_len]
    
    chunks = []
    current_idx = 0
    for i in range(len(ratios) - 1):
        target_len = int(ratios[i] * kor_len)
        target_idx = current_idx + target_len
        
        # Find closest boundary
        closest_b = min(boundaries, key=lambda x: abs(x - target_idx))
        
        # If closest boundary is <= current_idx or >= kor_len, just use target_idx
        if closest_b <= current_idx or closest_b >= kor_len:
            closest_b = target_idx
            
        chunks.append(korean_original[current_idx:closest_b])
        current_idx = closest_b
        
    chunks.append(korean_original[current_idx:])
    
    return chunks

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch10_tasks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

aligned = []
for item in data:
    chunks = proportional_split(item['english_chunks'], item['korean_original'])
    aligned.append({
        'paragraph_index': item['paragraph_index'],
        'korean_chunks': chunks
    })

with open('c:/git_repo/TKprof_book/books/dracula/chunk_tasks/ch10_aligned.json', 'w', encoding='utf-8') as f:
    json.dump(aligned, f, ensure_ascii=False, indent=2)

print('Success')
