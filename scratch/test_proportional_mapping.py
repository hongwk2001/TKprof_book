import re

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def get_words(text):
    return re.findall(r'\b\w+\b', text.lower())

def main():
    raw_path = 'books/dracula/chapters_backup/raw_ch_21.txt'
    en_path = 'books/dracula/chapters/ch21_en.txt'
    
    raw_p = paras(raw_path)
    en_p = paras(en_path)
    
    raw_words = [get_words(p) for p in raw_p]
    en_words = [get_words(p) for p in en_p]
    
    total_raw_words = sum(len(w) for w in raw_words)
    total_en_words = sum(len(w) for w in en_words)
    
    # Cumulative word intervals for raw paragraphs (0-based word indices)
    raw_intervals = []
    curr = 0
    for w in raw_words:
        raw_intervals.append((curr, curr + len(w)))
        curr += len(w)
        
    # Map each word of the chunked English to a raw paragraph index
    # We create a mapping: flat_en_word_index -> raw_para_index
    en_word_to_raw_para = []
    for w_en_idx in range(total_en_words):
        # Proportional position
        pos = (w_en_idx + 0.5) / total_en_words
        raw_pos = pos * total_raw_words
        
        # Find which raw paragraph this word falls into
        matched_r = 0
        for r_idx, (start, end) in enumerate(raw_intervals):
            if start <= raw_pos < end:
                matched_r = r_idx
                break
        else:
            matched_r = len(raw_p) - 1
        en_word_to_raw_para.append(matched_r)
        
    # Now, for each chunked paragraph, collect the raw paragraphs its words mapped to
    chunk_to_raw_mapped = []
    w_curr = 0
    for e_idx, w_list in enumerate(en_words):
        w_len = len(w_list)
        if w_len == 0:
            # Empty paragraph (e.g. title) - map to adjacent
            chunk_to_raw_mapped.append([])
            continue
            
        mapped_raws = en_word_to_raw_para[w_curr : w_curr + w_len]
        w_curr += w_len
        
        # Count occurrences of each raw para
        counts = {}
        for r in mapped_raws:
            counts[r] = counts.get(r, 0) + 1
            
        # Filter raw paras: must have >= 15% of the paragraph's words,
        # or be the maximum match.
        max_r = max(counts, key=counts.get)
        kept_raws = []
        for r, count in counts.items():
            if count >= 0.15 * w_len or r == max_r:
                kept_raws.append(r)
                
        chunk_to_raw_mapped.append(sorted(kept_raws))

    # Clean up mapping to enforce monotonicity and completeness
    # Ensure every chunk has at least one mapped raw para
    for e_idx in range(len(en_p)):
        if not chunk_to_raw_mapped[e_idx]:
            # Use mapping from previous or next chunk
            if e_idx > 0:
                chunk_to_raw_mapped[e_idx] = [chunk_to_raw_mapped[e_idx-1][-1]]
            else:
                chunk_to_raw_mapped[e_idx] = [0]

    # Map each raw paragraph to the chunked paragraphs that contain it
    raw_to_chunks = {}
    for e_idx, r_list in enumerate(chunk_to_raw_mapped):
        for r in r_list:
            raw_to_chunks.setdefault(r, []).append(e_idx)
            
    # Generate new IDs
    new_ids = [None] * len(en_p)
    
    for e_idx, r_list in enumerate(chunk_to_raw_mapped):
        r_first = r_list[0]
        r_last = r_list[-1]
        
        if r_first == r_last:
            # This chunk maps to exactly one raw paragraph `r_first`
            # Check if `r_first` is split across multiple chunked paragraphs
            chunks_for_r = raw_to_chunks.get(r_first, [])
            if len(chunks_for_r) <= 1:
                # 1-to-1
                new_ids[e_idx] = f"P{r_first+1:03d}"
            else:
                # Split: assign suffixes a, b, c...
                sub_idx = chunks_for_r.index(e_idx)
                suffix = chr(ord('a') + sub_idx)
                new_ids[e_idx] = f"P{r_first+1:03d}{suffix}"
        else:
            # Merged paragraph: maps to range from r_first to r_last
            new_ids[e_idx] = f"P{r_first+1:03d}_{r_last+1:03d}"
            
    # Print results
    for e_idx in range(len(en_p)):
        r_list = chunk_to_raw_mapped[e_idx]
        r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
        print(f"C{e_idx+1:02d}: [{e_idx+1:03d} -> {new_ids[e_idx]}] | Maps to raw: {r_str} | Preview: {en_p[e_idx][:60]}...")

if __name__ == '__main__':
    main()
