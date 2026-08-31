import os
import re

def strip_tags(text):
    # Strip any paragraph ID tag like [P001], [P011a], or [P010_011] from the start
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def word_count(text):
    return len(text.split())

def get_keywords(text):
    stopwords = {'the','a','an','and','or','but','of','to','in','on','at','by','for',
                 'with','about','as','it','its','he','him','his','she','her','they',
                 'them','their','i','me','my','we','us','our','you','your','was','were',
                 'is','are','been','be','have','has','had','do','does','did','that',
                 'this','there','then','so','if','out','up','down','no','not'}
    # Use [a-zA-Z0-9]+ instead of \w+ to ignore formatting underscores like _Wednesday_
    words = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return set(w for w in words if w not in stopwords)

def is_divider(text):
    # Strip tags and check if the remainder has no letters/numbers but contains *
    clean = re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())
    return not re.search(r'[a-zA-Z0-9가-힣]', clean) and '*' in clean

def map_and_tag_chapter(ch_idx):
    ch = f"{ch_idx:02d}"
    raw_path = f'books/dracula/chapters_backup/raw_ch_{ch}.txt'
    en_path = f'books/dracula/chapters/ch{ch}_en.txt'
    ko_path = f'books/dracula/chapters/ch{ch}_ko.txt'
    
    if not os.path.exists(raw_path):
        print(f"Skipping Ch {ch}: raw file not found at {raw_path}")
        return False
    if not os.path.exists(en_path) or not os.path.exists(ko_path):
        print(f"Skipping Ch {ch}: bilingual files not found")
        return False
        
    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_paras = [strip_tags(p) for p in f.read().split('\n\n') if p.strip()]
        
    with open(en_path, 'r', encoding='utf-8') as f:
        en_paras = [strip_tags(p) for p in f.read().split('\n\n') if p.strip()]
        
    with open(ko_path, 'r', encoding='utf-8') as f:
        ko_paras = [strip_tags(p) for p in f.read().split('\n\n') if p.strip()]
        
    if len(en_paras) != len(ko_paras):
        print(f"ERROR: Ch {ch} parity mismatch! EN={len(en_paras)}, KO={len(ko_paras)}")
        return False
        
    n_raw = len(raw_paras)
    n_en = len(en_paras)
    
    # ===== Global DP Alignment: Midpoint Ratio + Keyword Overlap =====
    raw_wc = [word_count(p) for p in raw_paras]
    en_wc  = [word_count(p) for p in en_paras]

    raw_cumul, s = [], 0
    for w in raw_wc:
        s += w; raw_cumul.append(s)
    raw_start = [0] + raw_cumul[:-1]
    total_raw = raw_cumul[-1]

    en_cumul, s = [], 0
    for w in en_wc:
        s += w; en_cumul.append(s)
    en_start = [0] + en_cumul[:-1]
    total_en = en_cumul[-1]

    raw_kw = [get_keywords(p) for p in raw_paras]
    en_kw  = [get_keywords(p) for p in en_paras]

    # DP matrix
    DP = [[float('inf')] * n_raw for _ in range(n_en)]
    parent = [[-1] * n_raw for _ in range(n_en)]

    def cost(j, i):
        en_div = is_divider(en_paras[j])
        raw_div = is_divider(raw_paras[i])
        
        # Strict Divider Anchoring
        if en_div and raw_div:
            return -1000.0
        elif en_div or raw_div:
            return 1000.0
            
        en_mid = (en_start[j] + en_cumul[j]) / 2.0
        en_ratio = en_mid / max(1, total_en)
        raw_mid = (raw_start[i] + raw_cumul[i]) / 2.0
        raw_ratio = raw_mid / max(1, total_raw)
        
        dist = abs(en_ratio - raw_ratio)
        overlap = len(en_kw[j].intersection(raw_kw[i]))
        
        # Base penalty is the distance. 
        # We multiply by 100 so a 0.01 ratio difference is 1 cost unit.
        # Each overlapping keyword reduces cost by 20 units.
        return (dist * 100.0) - (overlap * 20.0)

    for i in range(n_raw):
        DP[0][i] = cost(0, i)

    for j in range(1, n_en):
        for i in range(n_raw):
            best_prev = float('inf')
            best_k = -1
            # Previous EN para j-1 must map to k <= i
            search_start = max(0, i - 15)
            for k in range(search_start, i + 1):
                if DP[j-1][k] < best_prev:
                    best_prev = DP[j-1][k]
                    best_k = k
            DP[j][i] = best_prev + cost(j, i)
            parent[j][i] = best_k

    # Backtrack
    best_last = float('inf')
    curr_i = -1
    for i in range(n_raw):
        if DP[n_en-1][i] < best_last:
            best_last = DP[n_en-1][i]
            curr_i = i

    en_to_raw_single = [0] * n_en
    for j in range(n_en-1, -1, -1):
        en_to_raw_single[j] = curr_i
        curr_i = parent[j][curr_i]

    # ===== Build mapping lists, gap-fill, generate IDs =====
    en_to_raw = [[x] for x in en_to_raw_single]
    for r in range(n_raw):
        if not any(r in en_to_raw[j] for j in range(n_en)):
            merged = False
            for j in range(n_en):
                if en_to_raw_single[j] > r:
                    en_to_raw[j].append(r)
                    en_to_raw[j].sort()
                    merged = True
                    break
            if not merged:
                en_to_raw[-1].append(r)
                en_to_raw[-1].sort()
                
    # Build raw_to_en mapping to find splits
    raw_to_en = {}
    for j in range(n_en):
        for r in en_to_raw[j]:
            raw_to_en.setdefault(r, []).append(j)
            
    # Generate new mapped paragraph IDs
    new_ids = [None] * n_en
    for j in range(n_en):
        r_list = en_to_raw[j]
        r_first = r_list[0]
        r_last = r_list[-1]
        
        if r_first == r_last:
            # Single raw para
            chunks = raw_to_en[r_first]
            if len(chunks) == 1:
                new_ids[j] = f"P{r_first+1:03d}"
            else:
                # Split: assign suffixes a, b, c...
                sub_idx = chunks.index(j)
                suffix = chr(ord('a') + sub_idx)
                new_ids[j] = f"P{r_first+1:03d}{suffix}"
        else:
            # Merged range (e.g. P010_011)
            new_ids[j] = f"P{r_first+1:03d}_{r_last+1:03d}"
            
    # Apply tags and write files back
    tagged_en = [f"[{new_ids[j]}] {en_paras[j]}" for j in range(n_en)]
    tagged_ko = [f"[{new_ids[j]}] {ko_paras[j]}" for j in range(n_en)]
    
    with open(en_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(tagged_en))
        
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(tagged_ko))
        
    print(f"Successfully re-tagged Ch {ch}: {n_en} paragraphs mapped to {n_raw} raw.")
    return True

def main():
    print("Starting paragraph re-tagging process for Dracula...")
    success_count = 0
    for i in range(1, 28):
        if map_and_tag_chapter(i):
            success_count += 1
    print(f"Finished! Successfully re-tagged {success_count}/27 chapters.")

if __name__ == '__main__':
    main()
