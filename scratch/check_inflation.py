import re
import os

def clean_tag(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def word_count(text):
    return len(re.findall(r'\b\w+\b', text))

def parse_tag(tag):
    # tag can be 'P123', 'P123a', 'P123_124', etc.
    # We want to extract the base raw indexes (1-indexed)
    # Let's find all numbers in the tag
    m = re.match(r'^P(\d+)', tag)
    if m:
        # Check if it is a range like P012_013
        parts = tag[1:].split('_')
        try:
            indices = [int(p.strip('abcdefghijklmnopqrstuvwxyz')) for p in parts if p.strip('abcdefghijklmnopqrstuvwxyz')]
            if len(indices) == 2:
                return list(range(indices[0], indices[1] + 1))
            elif len(indices) == 1:
                return [indices[0]]
        except Exception:
            pass
        return [int(m.group(1))]
    return []

def analyze_chapter(ch):
    raw_path = f'books/dracula/chapters_backup/raw_ch_{ch}.txt'
    en_path = f'books/dracula/chapters/ch{ch}_en.txt'
    
    if not os.path.exists(raw_path) or not os.path.exists(en_path):
        print(f"File missing for Ch {ch}")
        return
        
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    with open(en_path, 'r', encoding='utf-8') as f:
        en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    print(f"=== Chapter {ch} Analysis ===")
    print(f"Raw Paras: {len(raw_paras)}, Chunked Paras: {len(en_paras)}")
    
    # We will map each chunked paragraph to the raw paragraph(s) it claims to map to.
    mapping = []
    for j, ep in enumerate(en_paras, 1):
        m = re.match(r'^\[(P[0-9a-zA-Z_]+)\]', ep)
        if not m:
            continue
        tag = m.group(1)
        raw_indices = parse_tag(tag)
        
        # Get raw text
        raw_text_parts = []
        for idx in raw_indices:
            # 1-indexed to 0-indexed
            raw_idx = idx - 1
            if 0 <= raw_idx < len(raw_paras):
                raw_text_parts.append(raw_paras[raw_idx])
        
        raw_text = ' '.join(raw_text_parts)
        en_text = clean_tag(ep)
        
        w_raw = word_count(raw_text)
        w_en = word_count(en_text)
        diff = w_en - w_raw
        ratio = w_en / w_raw if w_raw > 0 else 0
        
        mapping.append({
            'idx': j,
            'tag': tag,
            'w_raw': w_raw,
            'w_en': w_en,
            'diff': diff,
            'ratio': ratio,
            'en_snippet': en_text[:80],
            'raw_snippet': raw_text[:80]
        })
        
    # Sort by diff descending
    mapping.sort(key=lambda x: x['diff'], reverse=True)
    
    print("\nTop 10 most inflated paragraphs:")
    print(f"{'Para #':<6} | {'Tag':<10} | {'Raw W':<5} | {'EN W':<5} | {'Diff':<5} | {'Ratio':<6} | {'Snippet'}")
    print("-" * 80)
    for item in mapping[:10]:
        print(f"{item['idx']:<6} | {item['tag']:<10} | {item['w_raw']:<5} | {item['w_en']:<5} | {item['diff']:+5} | {item['ratio']:.2f}x | {item['en_snippet']}...")

def main():
    analyze_chapter('13')
    print("\n" + "="*50 + "\n")
    analyze_chapter('15')

if __name__ == '__main__':
    main()
