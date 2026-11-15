import json
import re
import itertools

with open('books/dracula/chunk_tasks/ch12_tasks.json', 'r', encoding='utf-8') as f:
    tasks = json.load(f)

def align(tasks):
    aligned_tasks = []
    for i, task in enumerate(tasks):
        eng_chunks = task['english_chunks']
        kor = task['korean_original']
        
        splits = []
        for match in re.finditer(r'[.!?][\"\'”’]?\s+', kor):
            splits.append(match.end())
            
        sentences = []
        start = 0
        for sp in splits:
            sentences.append(kor[start:sp])
            start = sp
        if start < len(kor):
            sentences.append(kor[start:])
            
        sentences = [s for s in sentences if s.strip()]
        
        eng_lens = [len(c) for c in eng_chunks]
        total_eng = sum(eng_lens)
        
        num_chunks = len(eng_chunks)
        if num_chunks == 1 or len(sentences) < num_chunks:
            # fallback
            best_split = [kor] + [""] * (num_chunks - 1)
            aligned_tasks.append({
                "paragraph_index": task["paragraph_index"],
                "korean_chunks": best_split
            })
            continue
            
        best_split = None
        best_error = float('inf')
        
        split_indices = list(range(1, len(sentences)))
        for sp_combo in itertools.combinations(split_indices, num_chunks - 1):
            start = 0
            kor_chunks = []
            for sp in sp_combo:
                kor_chunks.append("".join(sentences[start:sp]))
                start = sp
            kor_chunks.append("".join(sentences[start:]))
            
            kor_lens = [len(c) for c in kor_chunks]
            total_kor = sum(kor_lens)
            
            error = 0
            for k_len, e_len in zip(kor_lens, eng_lens):
                k_ratio = k_len / total_kor if total_kor > 0 else 0
                e_ratio = e_len / total_eng if total_eng > 0 else 0
                error += abs(k_ratio - e_ratio)
                
            if error < best_error:
                best_error = error
                best_split = kor_chunks
                
        aligned_tasks.append({
            "paragraph_index": task["paragraph_index"],
            "korean_chunks": [c.strip() for c in best_split]
        })
        
    return aligned_tasks

aligned = align(tasks)
with open('books/dracula/chunk_tasks/ch12_aligned.json', 'w', encoding='utf-8') as f:
    json.dump(aligned, f, ensure_ascii=False, indent=2)

print("Done alignment!")
