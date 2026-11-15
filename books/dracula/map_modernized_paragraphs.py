import os
import re

def get_words(text):
    # Remove tags like [P001]
    text = re.sub(r'\[P\d+\]', '', text)
    return re.findall(r'\b\w+\b', text.lower())

def map_modernized_chapter(ch_num):
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
        
    # Calculate word counts and cumulative word counts for raw
    raw_word_counts = [len(get_words(p)) for p in raw_paras]
    total_raw_words = sum(raw_word_counts)
    
    raw_intervals = []
    curr = 0
    for wc in raw_word_counts:
        raw_intervals.append((curr, curr + wc))
        curr += wc
        
    # Calculate word counts and cumulative word counts for chunked English
    en_word_counts = [len(get_words(p)) for p in en_paras]
    total_en_words = sum(en_word_counts)
    
    en_intervals = []
    curr = 0
    for wc in en_word_counts:
        en_intervals.append((curr, curr + wc))
        curr += wc
        
    mapping = []
    
    # Map intervals by percentage of total word count
    for raw_idx, (r_start, r_end) in enumerate(raw_intervals, 1):
        r_start_pct = r_start / total_raw_words
        r_end_pct = r_end / total_raw_words
        
        matched_chunk_paras = []
        
        for en_idx, (e_start, e_end) in enumerate(en_intervals, 1):
            e_start_pct = e_start / total_en_words
            e_end_pct = e_end / total_en_words
            
            # Check for overlap in percentage intervals
            # Standard interval overlap condition: max(start1, start2) < min(end1, end2)
            # We add a small epsilon to avoid mapping purely boundary-touching paragraphs
            overlap_start = max(r_start_pct, e_start_pct)
            overlap_end = min(r_end_pct, e_end_pct)
            
            if overlap_start < overlap_end - 1e-9:
                matched_chunk_paras.append(en_idx)
                
        # If no overlap found (e.g. empty paragraphs), find the closest one
        if not matched_chunk_paras:
            closest_idx = 1
            min_dist = 1.0
            mid_r = (r_start_pct + r_end_pct) / 2
            for en_idx, (e_start, e_end) in enumerate(en_intervals, 1):
                mid_e = (e_start / total_en_words + e_end / total_en_words) / 2
                dist = abs(mid_r - mid_e)
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = en_idx
            matched_chunk_paras.append(closest_idx)
            
        mapping.append({
            'raw_idx': raw_idx,
            'raw_words': raw_word_counts[raw_idx-1],
            'matched_paras': matched_chunk_paras,
            'matched_words': sum(en_word_counts[p-1] for p in matched_chunk_paras),
            'raw_text_preview': raw_paras[raw_idx-1][:80] + "..." if len(raw_paras[raw_idx-1]) > 80 else raw_paras[raw_idx-1]
        })
        
    # Generate markdown report
    report = []
    report.append(f"# Proportional Paragraph Mapping: Chapter {ch}")
    report.append(f"**Raw Words:** {total_raw_words:,} ({len(raw_paras)} paras) | **Chunked/Modernized Words:** {total_en_words:,} ({len(en_paras)} paras)")
    report.append(f"**Word Count Ratio (Modern/Raw):** {total_en_words / total_raw_words:.2f}x")
    report.append("")
    report.append("| Raw Para | Raw Words | Matched Chunk Paras | Chunked Words | Ratio | Raw Preview |")
    report.append("|----------|-----------|----------------------|---------------|-------|-------------|")
    
    for m in mapping:
        paras_str = ", ".join(f"P{p:03d}" for p in m['matched_paras'])
        ratio = m['matched_words'] / m['raw_words'] if m['raw_words'] else 0.0
        ratio_str = f"{ratio:.2f}x"
        report.append(f"| P{m['raw_idx']:03d} | {m['raw_words']} | {paras_str} | {m['matched_words']} | {ratio_str} | {m['raw_text_preview']} |")
        
    return "\n".join(report)

if __name__ == '__main__':
    # Map Chapter 9 (high modernization mismatch)
    report = map_modernized_chapter(9)
    artifact_path = r'C:\Users\hongw\.gemini\antigravity\brain\b85acb0a-6fb8-4473-bf15-263a48b385aa\modernized_mapping_ch09.md'
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Report saved to {artifact_path}")
