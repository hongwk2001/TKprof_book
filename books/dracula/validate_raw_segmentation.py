import os
import re

def get_words(text):
    # Remove paragraph tags like [P001]
    text = re.sub(r'\[P\d+\]', '', text)
    # Lowercase and find all word tokens (ignoring punctuation)
    return re.findall(r'\b\w+\b', text.lower())

def validate():
    base = 'books/dracula/chapters'
    raw_source_path = 'books/dracula/raw_source.txt'
    
    if not os.path.exists(raw_source_path):
        print(f"Error: {raw_source_path} not found.")
        return
        
    with open(raw_source_path, 'r', encoding='utf-8') as f:
        source_content = f.read()
        
    source_words = get_words(source_content)
    
    chapter_words = {}
    combined_words = []
    
    print("Chapter-by-Chapter Word Counts:")
    print("-" * 40)
    for i in range(1, 28):
        ch = f'{i:02d}'
        ch_path = os.path.join(base, f'raw_ch_{ch}.txt')
        if not os.path.exists(ch_path):
            print(f"Ch {ch}: File not found!")
            continue
            
        with open(ch_path, 'r', encoding='utf-8') as f:
            ch_content = f.read()
            
        ch_words = get_words(ch_content)
        chapter_words[i] = len(ch_words)
        combined_words.extend(ch_words)
        print(f"Chapter {ch}: {len(ch_words):,} words")
        
    total_chapters_words = len(combined_words)
    print("-" * 40)
    print(f"Total Chapters Combined: {total_chapters_words:,} words\n")
    
    # Locate where the combined chapters start in raw_source
    # We use a sliding window of the first 30 words to find the starting index
    prefix_len = 30
    prefix = combined_words[:prefix_len]
    
    candidates = []
    for idx in range(len(source_words) - prefix_len):
        if source_words[idx : idx + prefix_len] == prefix:
            candidates.append(idx)
            
    if not candidates:
        print("Error: Could not find the beginning of Chapter 1 in the raw source text.")
        return
        
    # If there are multiple candidates (e.g. TOC), find the one that matches the longest sequence
    best_start = -1
    max_match_len = 0
    for cand in candidates:
        # Check how far the match goes
        match_len = 0
        limit = min(len(combined_words), len(source_words) - cand)
        # Check in chunks of 100 for speed
        chunk_size = 100
        for offset in range(0, limit, chunk_size):
            end = min(offset + chunk_size, limit)
            if source_words[cand + offset : cand + end] == combined_words[offset : end]:
                match_len = end
            else:
                # Find exact mismatch point in this chunk
                for i in range(offset, end):
                    if source_words[cand + i] == combined_words[i]:
                        match_len = i + 1
                    else:
                        break
                break
        if match_len > max_match_len:
            max_match_len = match_len
            best_start = cand
            
    print(f"Best start index found in raw_source: {best_start} (out of {len(source_words)} total words)")
    
    # Check if we have a perfect match
    if max_match_len == total_chapters_words:
        print("✅ SUCCESS: The 27 raw chapters perfectly match raw_source.txt sequentially!")
        print(f"Core Narrative Range in raw_source: words {best_start:,} to {best_start + total_chapters_words:,}")
        print(f"Raw Source Total Words: {len(source_words):,}")
        print(f"Matched Narrative Words: {total_chapters_words:,}")
    else:
        print(f"❌ FAILURE: Mismatch detected at offset {max_match_len:,} from start of narrative.")
        
        # Print surrounding context of the mismatch
        mismatch_idx_source = best_start + max_match_len
        mismatch_idx_ch = max_match_len
        
        print("\n--- Source Context (raw_source.txt) ---")
        source_context = source_words[max(0, mismatch_idx_source - 10) : min(len(source_words), mismatch_idx_source + 15)]
        print("... " + " ".join(source_context) + " ...")
        print("Mismatch word in Source:", source_words[mismatch_idx_source] if mismatch_idx_source < len(source_words) else "EOF")
        
        print("\n--- Chapters Context (raw_ch_XX.txt) ---")
        ch_context = combined_words[max(0, mismatch_idx_ch - 10) : min(len(combined_words), mismatch_idx_ch + 15)]
        print("... " + " ".join(ch_context) + " ...")
        print("Mismatch word in Chapters:", combined_words[mismatch_idx_ch] if mismatch_idx_ch < len(combined_words) else "EOF")
        
        # Try to locate which chapter contains the mismatch
        accum = 0
        for ch_num, w_count in chapter_words.items():
            if accum <= mismatch_idx_ch < accum + w_count:
                relative_offset = mismatch_idx_ch - accum
                print(f"\nMismatch lies inside Chapter {ch_num:02d} at word offset {relative_offset:,} of that chapter.")
                break
            accum += w_count

if __name__ == '__main__':
    validate()
