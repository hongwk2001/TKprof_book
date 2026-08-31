import re

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def get_words(text):
    # Strip common small stop words to focus on content words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'of', 'to', 'in', 'on', 'at', 'by', 'for', 'with', 'about', 'as', 'it', 'its', 'he', 'him', 'his', 'she', 'her', 'they', 'them', 'their', 'i', 'me', 'my', 'we', 'us', 'our', 'you', 'your', 'was', 'were', 'is', 'are', 'been', 'be', 'have', 'has', 'had', 'do', 'does', 'did', 'that', 'this', 'there', 'then', 'so', 'if', 'out', 'up', 'down', 'no', 'not'}
    words = re.findall(r'\b\w+\b', text.lower())
    return set(w for w in words if w not in stopwords)

def main():
    raw_path = 'books/dracula/chapters_backup/raw_ch_21.txt'
    en_path = 'books/dracula/chapters/ch21_en.txt'
    
    raw_p = paras(raw_path)
    en_p = paras(en_path)
    
    raw_words = [get_words(p) for p in raw_p]
    en_words = [get_words(p) for p in en_p]
    
    n_raw = len(raw_p)
    n_en = len(en_p)
    
    dp = [[-1000000] * (n_en + 1) for _ in range(n_raw + 1)]
    parent = [[None] * (n_en + 1) for _ in range(n_raw + 1)]
    
    dp[0][0] = 0
    
    # We want to match.
    # Cost: word overlap - proximity penalty
    # Proximity penalty: 1.5 * |i - j * (n_raw / n_en)|
    
    for i in range(n_raw + 1):
        for j in range(n_en + 1):
            if dp[i][j] < -500000:
                continue
                
            # Match raw[i] with en[j]
            if i < n_raw and j < n_en:
                overlap = len(raw_words[i].intersection(en_words[j]))
                expected_raw_idx = j * (n_raw / n_en)
                dist = abs(i - expected_raw_idx)
                # Let's adjust weight
                score = overlap - 2.5 * dist
                if dp[i][j] + score > dp[i+1][j+1]:
                    dp[i+1][j+1] = dp[i][j] + score
                    parent[i+1][j+1] = (i, j, 'match')
                    
            # Merge raw[i] into current en[j-1]
            if i < n_raw and j > 0:
                overlap = len(raw_words[i].intersection(en_words[j-1]))
                expected_raw_idx = (j-1) * (n_raw / n_en)
                dist = abs(i - expected_raw_idx)
                score = overlap - 2.5 * dist
                if dp[i][j] + score > dp[i+1][j]:
                    dp[i+1][j] = dp[i][j] + score
                    parent[i+1][j] = (i, j, 'merge')
                    
            # Split raw[i-1] into en[j]
            if i > 0 and j < n_en:
                overlap = len(raw_words[i-1].intersection(en_words[j]))
                expected_raw_idx = j * (n_raw / n_en)
                dist = abs((i-1) - expected_raw_idx)
                score = overlap - 2.5 * dist
                if dp[i][j] + score > dp[i][j+1]:
                    dp[i][j+1] = dp[i][j] + score
                    parent[i][j+1] = (i, j, 'split')
                    
    # Backtrack
    curr_i, curr_j = n_raw, n_en
    alignments = []
    
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
    
    en_to_raw = {}
    for r, e in alignments:
        en_to_raw.setdefault(e, set()).add(r)
        
    raw_to_en = {}
    for e in range(n_en):
        r_list = sorted(list(en_to_raw.get(e, set())))
        if not r_list:
            if e > 0:
                r_list = [en_to_raw.get(e-1, [0])[-1]]
            else:
                r_list = [0]
        en_to_raw[e] = r_list
        for r in r_list:
            raw_to_en.setdefault(r, []).append(e)
            
    new_ids = [None] * n_en
    for e in range(n_en):
        r_list = en_to_raw[e]
        r_first = r_list[0]
        r_last = r_list[-1]
        
        if r_first == r_last:
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
            
    # Print results
    for e in range(n_en):
        r_list = en_to_raw[e]
        r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
        print(f"C{e+1:02d}: [{e+1:03d} -> {new_ids[e]}] | Maps to raw: {r_str} | Preview: {en_p[e][:60]}...")

if __name__ == '__main__':
    main()
