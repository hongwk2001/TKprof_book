import re
import os

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def run_prototype():
    raw_path = 'books/dracula/chapters_backup/raw_ch_21.txt'
    en_path = 'books/dracula/chapters/ch21_en.txt'
    ko_path = 'books/dracula/chapters/ch21_ko.txt'
    
    raw_p = paras(raw_path)
    en_p = paras(en_path)
    ko_p = paras(ko_path)
    
    # Let's perform sequence alignment (using a simple LCS-like or sliding window word overlap)
    # since we want to align raw_p (69 paras) with en_p (64 paras).
    # We will compute word similarity and align sequentially to preserve order.
    
    # 1. Clean words for each paragraph
    def get_words(text):
        return re.findall(r'\b\w+\b', text.lower())
        
    raw_words_lists = [get_words(p) for p in raw_p]
    en_words_lists = [get_words(p) for p in en_p]
    
    # Let's align using a dynamic programming / sequence alignment approach
    # We want to map each chunked paragraph to the raw paragraph(s) that overlap with it the most
    # maintaining strict order (monotonicity).
    
    # Let's map each raw paragraph to one or more chunked paragraphs
    # Since we have total_raw_words and total_en_words, we can also use word prefix indices to map them.
    raw_flat = []
    for r_idx, r_words in enumerate(raw_words_lists):
        for w in r_words:
            raw_flat.append((r_idx, w))
            
    en_flat = []
    for e_idx, e_words in enumerate(en_words_lists):
        for w in e_words:
            en_flat.append((e_idx, w))
            
    # For each word in en_flat, we map it to the raw_flat word at the same proportional position
    mapping = {} # en_idx -> set of raw_idx
    
    for i, (e_idx, w) in enumerate(en_flat):
        # proportional position
        pct = i / len(en_flat)
        r_flat_idx = int(pct * len(raw_flat))
        r_flat_idx = min(r_flat_idx, len(raw_flat) - 1)
        r_idx = raw_flat[r_flat_idx][0]
        mapping.setdefault(e_idx, set()).add(r_idx)
        
    # Let's refine the mapping to be contiguous and strictly monotonic
    # (i.e. en_idx 0 maps to raw_idx 0, en_idx 63 maps to raw_idx 68)
    # Let's print out the raw mapping first
    aligned_mapping = []
    for e_idx in range(len(en_p)):
        raw_set = mapping.get(e_idx, set())
        aligned_mapping.append((e_idx, sorted(list(raw_set))))
        
    # Let's make sure the mapping is clean. 
    # Since we want to show a clear prototype, let's write a heuristic alignment based on the start words
    # of the raw paragraphs and chunked paragraphs.
    # Let's use a simpler heuristic: look for unique sentence/phrase matches
    # or just simple sequential matching with backtracking.
    # Actually, let's use the proportional window:
    # A chunk paragraph e_idx maps to raw paragraph(s).
    # If a raw paragraph r_idx is mapped to multiple chunk paragraphs, say [e_1, e_2, e_3],
    # then they get labeled as r_idx+'a', r_idx+'b', r_idx+'c'.
    # If multiple raw paragraphs are mapped to a single chunk paragraph, it gets labeled with the first raw paragraph index.
    
    # Let's write a robust monotonic alignment:
    # We want to find a mapping M: C -> R (each chunked maps to a set of raw, maintaining order)
    # Let's use a DP to align the paragraphs based on word similarities
    n_raw = len(raw_p)
    n_en = len(en_p)
    
    # dp[i][j] is the cost/score of aligning first i raw paragraphs with first j en paragraphs
    # We want to maximize similarity.
    # score of matching raw i to en j is the number of shared words
    def similarity(r_words, e_words):
        if not r_words or not e_words:
            return 0
        r_set = set(r_words)
        e_set = set(e_words)
        return len(r_set.intersection(e_set))
        
    dp = [[-1] * (n_en + 1) for _ in range(n_raw + 1)]
    parent = [[None] * (n_en + 1) for _ in range(n_raw + 1)]
    
    dp[0][0] = 0
    
    for i in range(n_raw + 1):
        for j in range(n_en + 1):
            if dp[i][j] == -1:
                continue
            
            # Option 1: Match raw[i] with en[j] (one-to-one or starting a group)
            if i < n_raw and j < n_en:
                score = similarity(raw_words_lists[i], en_words_lists[j])
                if dp[i][j] + score > dp[i+1][j+1]:
                    dp[i+1][j+1] = dp[i][j] + score
                    parent[i+1][j+1] = (i, j, 'match')
                    
            # Option 2: Merge raw[i] into the current/next en[j] (many raw to one en)
            if i < n_raw and j > 0:
                score = similarity(raw_words_lists[i], en_words_lists[j-1])
                if dp[i][j] + score > dp[i+1][j]:
                    dp[i+1][j] = dp[i][j] + score
                    parent[i+1][j] = (i, j, 'merge_raw')
                    
            # Option 3: Split raw[i-1] to match next en[j] (one raw to many en)
            if i > 0 and j < n_en:
                score = similarity(raw_words_lists[i-1], en_words_lists[j])
                if dp[i][j] + score > dp[i][j+1]:
                    dp[i][j+1] = dp[i][j] + score
                    parent[i][j+1] = (i, j, 'split_en')
                    
    # Backtrack
    curr_i, curr_j = n_raw, n_en
    path = []
    while curr_i > 0 or curr_j > 0:
        if parent[curr_i][curr_j] is None:
            break
        prev_i, prev_j, action = parent[curr_i][curr_j]
        path.append((prev_i, prev_j, curr_i, curr_j, action))
        curr_i, curr_j = prev_i, prev_j
        
    path.reverse()
    
    # From the path, let's construct raw_to_en and en_to_raw mapping lists
    en_to_raw = [[] for _ in range(n_en)]
    for prev_i, prev_j, curr_i, curr_j, action in path:
        if action == 'match':
            en_to_raw[prev_j].append(prev_i)
        elif action == 'merge_raw':
            # raw raw[prev_i] is merged into en[prev_j-1]
            en_to_raw[prev_j-1].append(prev_i)
        elif action == 'split_en':
            # en[prev_j] is matched to raw[prev_i-1]
            en_to_raw[prev_j].append(prev_i-1)
            
    # Deduplicate and sort raw indices for each chunked paragraph
    for j in range(n_en):
        en_to_raw[j] = sorted(list(set(en_to_raw[j])))
        
    # Generate new ID strings
    # We want to find if a raw paragraph maps to multiple chunked paragraphs
    raw_to_en_count = {}
    for j, raw_list in enumerate(en_to_raw):
        for r in raw_list:
            raw_to_en_count.setdefault(r, []).append(j)
            
    new_ids = [None] * n_en
    
    for r, en_indices in raw_to_en_count.items():
        if len(en_indices) == 1:
            # 1-to-1 or merged raw paras
            j = en_indices[0]
            # If multiple raw paras merged into this one
            r_list = en_to_raw[j]
            if len(r_list) == 1:
                new_ids[j] = f"P{r+1:03d}"
            else:
                # Merge: e.g. R010 and R011 merged -> P010
                new_ids[j] = f"P{r_list[0]+1:03d}"
        else:
            # Split: raw r split into multiple en_indices
            # Label as P011a, P011b, etc.
            for sub_idx, j in enumerate(en_indices):
                suffix = chr(ord('a') + sub_idx)
                new_ids[j] = f"P{r+1:03d}{suffix}"
                
    # Print the mapping and new paragraph tags
    print("=== PROTOTYPE PARAGRAPH MAPPING FOR CH 21 ===")
    for j in range(n_en):
        r_list = en_to_raw[j]
        r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
        old_tag = f"[P{j+1:03d}]"
        new_tag = f"[{new_ids[j]}]"
        print(f"Chn Para {j+1:02d}: {old_tag} -> {new_tag} | Maps to raw: {r_str} | Preview: {en_p[j][:60]}...")

if __name__ == '__main__':
    run_prototype()
