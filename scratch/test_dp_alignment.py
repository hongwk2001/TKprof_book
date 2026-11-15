import re

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def get_words(text):
    return set(re.findall(r'\b\w+\b', text.lower()))

def main():
    raw_path = 'books/dracula/chapters_backup/raw_ch_21.txt'
    en_path = 'books/dracula/chapters/ch21_en.txt'
    
    raw_p = paras(raw_path)
    en_p = paras(en_path)
    
    raw_words = [get_words(p) for p in raw_p]
    en_words = [get_words(p) for p in en_p]
    
    n_raw = len(raw_p)
    n_en = len(en_p)
    
    # Let's define the DP table
    # dp[i][j] is the max word overlap score for aligning first i raw paras with first j en paras
    # We also enforce that we cannot skip paragraphs.
    dp = [[-100000] * (n_en + 1) for _ in range(n_raw + 1)]
    parent = [[None] * (n_en + 1) for _ in range(n_raw + 1)]
    
    dp[0][0] = 0
    
    # We want to match/align.
    # Cost function: intersection of words.
    # To encourage larger paragraphs to match, we can use the size of intersection.
    # To avoid random small matches, we add a tiny penalty for splitting/merging if they are not matching.
    
    for i in range(n_raw + 1):
        for j in range(n_en + 1):
            if dp[i][j] < -10000:
                continue
                
            # Transition 1: Match raw[i] with en[j]
            if i < n_raw and j < n_en:
                score = len(raw_words[i].intersection(en_words[j]))
                if dp[i][j] + score > dp[i+1][j+1]:
                    dp[i+1][j+1] = dp[i][j] + score
                    parent[i+1][j+1] = (i, j, 'match')
            
            # Transition 2: Merge raw[i] into the current en[j-1] (if j > 0)
            if i < n_raw and j > 0:
                # We are appending raw[i] to the match for en[j-1]
                # The score change is the overlap of raw[i] with en[j-1]
                score = len(raw_words[i].intersection(en_words[j-1]))
                if dp[i][j] + score > dp[i+1][j]:
                    dp[i+1][j] = dp[i][j] + score
                    parent[i+1][j] = (i, j, 'merge')
                    
            # Transition 3: Split raw[i-1] into en[j] (if i > 0)
            if i > 0 and j < n_en:
                # en[j] is matching raw[i-1]
                score = len(raw_words[i-1].intersection(en_words[j]))
                if dp[i][j] + score > dp[i][j+1]:
                    dp[i][j+1] = dp[i][j] + score
                    parent[i][j+1] = (i, j, 'split')
                    
    # Backtrack
    curr_i, curr_j = n_raw, n_en
    alignments = [] # list of (r_idx, e_idx)
    
    while curr_i > 0 or curr_j > 0:
        if parent[curr_i][curr_j] is None:
            break
        prev_i, prev_j, action = parent[curr_i][curr_j]
        if action == 'match':
            alignments.append((prev_i, prev_j))
        elif action == 'merge':
            alignments.append((prev_i, prev_j - 1))
        elif action == 'split':
            alignments.append((prev_i - 1, prev_j))
        curr_i, curr_j = prev_i, prev_j
        
    alignments.reverse()
    
    # Let's map each en paragraph to a list of raw paragraphs it aligns with
    en_to_raw = {}
    for r, e in alignments:
        en_to_raw.setdefault(e, set()).add(r)
        
    # Build a clean contiguous mapping
    # Every en paragraph must map to a list of raw paragraphs
    raw_to_en = {}
    for e in range(n_en):
        r_set = en_to_raw.get(e, set())
        r_list = sorted(list(r_set))
        if not r_list:
            # Fallback if unmapped: use neighbors
            if e > 0:
                r_list = [en_to_raw.get(e-1, {0})[-1]]
            else:
                r_list = [0]
        en_to_raw[e] = r_list
        for r in r_list:
            raw_to_en.setdefault(r, []).append(e)
            
    # Generate the tags
    new_ids = [None] * n_en
    for e in range(n_en):
        r_list = en_to_raw[e]
        r_first = r_list[0]
        r_last = r_list[-1]
        
        if r_first == r_last:
            # Check if this raw paragraph is split across multiple en paragraphs
            all_chunks_for_r = raw_to_en.get(r_first, [])
            if len(all_chunks_for_r) <= 1:
                new_ids[e] = f"P{r_first+1:03d}"
            else:
                sub_idx = all_chunks_for_r.index(e)
                suffix = chr(ord('a') + sub_idx)
                new_ids[e] = f"P{r_first+1:03d}{suffix}"
        else:
            # Merged paragraph
            new_ids[e] = f"P{r_first+1:03d}_{r_last+1:03d}"
            
    # Print out results to see if they align perfectly
    for e in range(n_en):
        r_list = en_to_raw[e]
        r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
        print(f"C{e+1:02d}: [{e+1:03d} -> {new_ids[e]}] | Maps to raw: {r_str} | Preview: {en_p[e][:60]}...")

if __name__ == '__main__':
    main()
