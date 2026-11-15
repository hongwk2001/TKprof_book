import json
import re
import os

def split_korean():
    task_file = 'books/dracula/chunk_tasks/ch10_tasks.json'
    out_file = 'books/dracula/chunk_tasks/ch10_aligned.json'
    
    with open(task_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    output = []
    
    for obj in data:
        korean = obj['korean_original']
        eng_chunks = obj['english_chunks']
        n = len(eng_chunks)
        
        # Calculate lengths of english chunks
        eng_lengths = [len(c) for c in eng_chunks]
        total_eng = sum(eng_lengths)
        proportions = [l / total_eng for l in eng_lengths]
        
        # Split Korean text based on proportions
        chunks = []
        start = 0
        kor_len = len(korean)
        
        # Find sentence boundaries in Korean text to make the splits cleaner
        matches = list(re.finditer(r'[.!?](?:["\']|)(?:\s+|\Z)', korean))
        valid_splits = [m.end() for m in matches]
        valid_splits.append(kor_len)
        
        for i in range(n - 1):
            target_len = int(kor_len * sum(proportions[:i+1]))
            # Find the closest valid split point
            if valid_splits:
                closest_split = min(valid_splits, key=lambda x: abs(x - target_len))
                # Remove used split points
                valid_splits = [x for x in valid_splits if x > closest_split]
            else:
                closest_split = target_len
            
            chunks.append(korean[start:closest_split])
            start = closest_split
            
        chunks.append(korean[start:])
        
        output.append({
            "paragraph_index": obj["paragraph_index"],
            "korean_chunks": chunks
        })
        
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    split_korean()
