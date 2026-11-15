import os
import re

def get_words(text):
    # Remove tags like [P001]
    text = re.sub(r'\[P\d+\]', '', text)
    # Extract alphanumeric words
    return re.findall(r'\b\w+\b', text.lower())

def map_chapter_paragraphs(ch_num):
    base = 'books/dracula/chapters'
    ch = f'{ch_num:02d}'
    
    raw_path = os.path.join(base, f'raw_ch_{ch}.txt')
    en_path = os.path.join(base, f'ch{ch}_en.txt')
    
    if not os.path.exists(raw_path) or not os.path.exists(en_path):
        return f"Error: Files for Ch {ch} do not exist."
        
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    with open(en_path, 'r', encoding='utf-8') as f:
        en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    # We want to match raw_paras[i] to one or more en_paras[j]
    mapping = []
    
    en_idx = 0
    en_words_flat = []
    # Build list of (para_idx, word) for all words in chunked English
    for idx, ep in enumerate(en_paras, 1):
        for w in get_words(ep):
            en_words_flat.append((idx, w))
            
    word_cursor = 0
    
    for raw_idx, rp in enumerate(raw_paras, 1):
        raw_words = get_words(rp)
        if not raw_words:
            continue
            
        matched_en_paras = set()
        matched_words = []
        
        # Consume words from the chunked English until we match the raw paragraph's words
        # (Using a relaxed length check since there could be tiny word differences in other chapters)
        target_len = len(raw_words)
        consumed = 0
        
        while consumed < target_len and word_cursor < len(en_words_flat):
            para_num, w = en_words_flat[word_cursor]
            matched_en_paras.add(para_num)
            matched_words.append(w)
            word_cursor += 1
            consumed += 1
            
        mapping.append({
            'raw_idx': raw_idx,
            'raw_text_preview': rp[:80] + "..." if len(rp) > 80 else rp,
            'raw_word_count': len(raw_words),
            'chunk_paras': sorted(list(matched_en_paras)),
            'chunk_word_count': len(matched_words),
            'mismatch': raw_words != matched_words
        })
        
    # Generate a markdown report of the mapping
    report = []
    report.append(f"# Paragraph Mapping Report: Chapter {ch}")
    report.append(f"**Raw Paragraph Count:** {len(raw_paras)} | **Chunked English Paragraph Count:** {len(en_paras)}")
    report.append("")
    report.append("| Raw Para # | Word Count | Chunked Para Range | Chunked Word Count | Match? | Raw Preview |")
    report.append("|------------|------------|---------------------|-------------------|--------|-------------|")
    
    for m in mapping:
        range_str = ", ".join(f"P{p:03d}" for p in m['chunk_paras'])
        match_str = "✅" if not m['mismatch'] else "❌ MISMATCH"
        report.append(f"| P{m['raw_idx']:03d} | {m['raw_word_count']} | {range_str} | {m['chunk_word_count']} | {match_str} | {m['raw_text_preview']} |")
        
    return "\n".join(report)

if __name__ == '__main__':
    # Map Chapter 1 and save the report
    report = map_chapter_paragraphs(1)
    artifact_path = r'C:\Users\hongw\.gemini\antigravity\brain\b85acb0a-6fb8-4473-bf15-263a48b385aa\paragraph_mapping_ch01.md'
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report saved to {artifact_path}")
