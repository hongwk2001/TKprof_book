import json
import re

def split_korean_proportionally(korean_text, english_chunks):
    # Find all sentence boundaries (like ., ?, !)
    sentences = re.split(r'(?<=[.?!])\s+', korean_text.strip())
    # If no spaces after punctuation, try a more aggressive split while keeping punctuation
    if len(sentences) == 1:
        sentences = re.split(r'(?<=[.?!])\s*', korean_text.strip())
        sentences = [s for s in sentences if s]

    # Calculate target proportions based on English chunks
    eng_lengths = [len(chunk) for chunk in english_chunks]
    total_eng = sum(eng_lengths)
    proportions = [l / total_eng for l in eng_lengths]
    
    total_kor_chars = sum(len(s) for s in sentences)
    
    korean_chunks = []
    current_chunk = []
    current_chunk_chars = 0
    chunk_idx = 0
    
    for i, sentence in enumerate(sentences):
        current_chunk.append(sentence)
        current_chunk_chars += len(sentence)
        
        # If we are not at the last chunk, and we have reached or exceeded the target proportion
        if chunk_idx < len(proportions) - 1:
            target_chars = proportions[chunk_idx] * total_kor_chars
            # Check if this sentence puts us over the target
            if current_chunk_chars >= target_chars:
                # Should we include this sentence or not?
                # For simplicity, just cut here
                korean_chunks.append(' '.join(current_chunk))
                chunk_idx += 1
                current_chunk = []
                current_chunk_chars = 0
                
    # Add the remaining sentences to the last chunk
    if current_chunk:
        if len(korean_chunks) < len(english_chunks):
            korean_chunks.append(' '.join(current_chunk))
        else:
            korean_chunks[-1] = korean_chunks[-1] + ' ' + ' '.join(current_chunk)
            
    # If we didn't create enough chunks (e.g. fewer sentences than chunks), pad with empty strings
    while len(korean_chunks) < len(english_chunks):
        korean_chunks.append("")
        
    # Re-join with original spacing (this naive approach might alter spaces slightly,
    # let's do a strict proportional split by characters if sentences are tricky, 
    # but the prompt requires valid JSON and semantic boundaries... 
    # Actually, let's just do character-based split rounded to the nearest sentence boundary in the original string).
    pass

def split_string_by_indices(text, indices):
    chunks = []
    last_idx = 0
    for idx in indices:
        chunks.append(text[last_idx:idx].strip())
        last_idx = idx
    chunks.append(text[last_idx:].strip())
    return chunks

def smart_split(korean_text, english_chunks):
    eng_lengths = [len(c) for c in english_chunks]
    total_eng = sum(eng_lengths)
    if total_eng == 0: return [korean_text] + [""]*(len(english_chunks)-1)
    
    # Cumulative target proportions
    cum_proportions = []
    cum = 0
    for l in eng_lengths[:-1]:
        cum += l
        cum_proportions.append(cum / total_eng)
        
    kor_len = len(korean_text)
    target_indices = [int(p * kor_len) for p in cum_proportions]
    
    # Find nearest sentence endings (. ! ?" )
    actual_indices = []
    for target in target_indices:
        # Search backwards and forwards for the nearest sentence ending
        best_idx = target
        min_dist = 999999
        for match in re.finditer(r'[.?!][\'"]?\s+', korean_text):
            idx = match.end()
            if abs(idx - target) < min_dist:
                min_dist = abs(idx - target)
                best_idx = idx
        actual_indices.append(best_idx)
        
    # Now split the string exactly, preserving all characters including spaces
    chunks = []
    last_idx = 0
    for idx in actual_indices:
        chunks.append(korean_text[last_idx:idx].strip())
        last_idx = idx
    chunks.append(korean_text[last_idx:].strip())
    
    # Edge case: Ensure no empty chunks if possible, but keep exact concatenation matching (excluding edge spaces)
    return chunks

def main():
    with open('books/dracula/chunk_tasks/ch12_tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
        
    results = []
    for task in tasks:
        kor = task['korean_original']
        eng = task['english_chunks']
        kor_chunks = smart_split(kor, eng)
        results.append({
            'paragraph_index': task['paragraph_index'],
            'korean_chunks': kor_chunks
        })
        
    with open('books/dracula/chunk_tasks/ch12_aligned.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
