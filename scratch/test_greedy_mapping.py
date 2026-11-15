import re

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def get_words(text):
    return re.findall(r'\b\w+\b', text.lower())

raw_p = paras('books/dracula/chapters_backup/raw_ch_21.txt')
en_p = paras('books/dracula/chapters/ch21_en.txt')

# Flatten chunked English words with their paragraph index (0-based)
en_words_flat = []
for e_idx, ep in enumerate(en_p):
    for w in get_words(ep):
        en_words_flat.append((e_idx, w))

word_cursor = 0
raw_to_en = {} # r_idx -> list of e_idx

for r_idx, rp in enumerate(raw_p):
    raw_words = get_words(rp)
    if not raw_words:
        continue
    
    target_len = len(raw_words)
    consumed = 0
    matched_en_paras = []
    
    while consumed < target_len and word_cursor < len(en_words_flat):
        e_idx, w = en_words_flat[word_cursor]
        if e_idx not in matched_en_paras:
            matched_en_paras.append(e_idx)
        word_cursor += 1
        consumed += 1
        
    raw_to_en[r_idx] = matched_en_paras

# Print mapping
en_to_raw = {}
for r_idx, e_indices in raw_to_en.items():
    for e_idx in e_indices:
        en_to_raw.setdefault(e_idx, []).append(r_idx)

# Determine the new IDs
new_ids = [None] * len(en_p)
for e_idx in range(len(en_p)):
    r_list = en_to_raw.get(e_idx, [])
    if not r_list:
        new_ids[e_idx] = "UNMAPPED"
    elif len(r_list) == 1:
        # 1-to-1 mapping
        r = r_list[0]
        # Check if this raw paragraph is mapped to multiple chunk paragraphs
        mapped_chunks = [k for k, v in raw_to_en.items() if e_idx in v]
        # Since r is the only raw para for this chunk, let's see if r is split across multiple chunks
        all_chunks_for_r = raw_to_en[r]
        if len(all_chunks_for_r) == 1:
            new_ids[e_idx] = f"P{r+1:03d}"
        else:
            sub_idx = all_chunks_for_r.index(e_idx)
            suffix = chr(ord('a') + sub_idx)
            new_ids[e_idx] = f"P{r+1:03d}{suffix}"
    else:
        # Multiple raw paragraphs merged into one chunk paragraph
        # Tag it with the range or just the first one
        # Let's see: if we use the first one:
        new_ids[e_idx] = f"P{r_list[0]+1:03d}"

# Print results
for e_idx in range(len(en_p)):
    r_list = en_to_raw.get(e_idx, [])
    r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
    print(f"C{e_idx+1:02d}: [{e_idx+1:03d} -> {new_ids[e_idx]}] | Maps to raw: {r_str} | Preview: {en_p[e_idx][:60]}...")
