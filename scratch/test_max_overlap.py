import re

def clean(text):
    text = re.sub(r'\[P\w+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

def get_words(text):
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
    
    # Initial mapping from chunk to closest raw (using window)
    en_to_raw_single = []
    
    for j in range(n_en):
        expected_i = int(j * (n_raw / n_en))
        w_start = max(0, expected_i - 4)
        w_end = min(n_raw, expected_i + 6)
        
        best_i = expected_i
        best_overlap = -1
        
        for i in range(w_start, w_end):
            overlap = len(en_words[j].intersection(raw_words[i]))
            if overlap > best_overlap:
                best_overlap = overlap
                best_i = i
        en_to_raw_single.append(best_i)

    # Enforce monotonicity
    for j in range(1, n_en):
        if en_to_raw_single[j] < en_to_raw_single[j-1]:
            en_to_raw_single[j] = en_to_raw_single[j-1]
            
    # Now, we do gap filling to construct en_to_raw mapping as lists
    en_to_raw = [[] for _ in range(n_en)]
    for j in range(n_en):
        en_to_raw[j].append(en_to_raw_single[j])
        
    # Find any unmapped raw paragraphs and merge them into the next mapped chunk
    for r in range(n_raw):
        # Is r mapped to any chunk?
        mapped = False
        for j in range(n_en):
            if r in en_to_raw[j]:
                mapped = True
                break
        if not mapped:
            # Find where it belongs. 
            # We merge it into the first chunk j that is mapped to a raw index > r
            merged = False
            for j in range(n_en):
                if en_to_raw_single[j] > r:
                    en_to_raw[j].append(r)
                    en_to_raw[j].sort()
                    merged = True
                    break
            if not merged:
                # Append to the last chunk
                en_to_raw[-1].append(r)
                en_to_raw[-1].sort()
                
    # Now build raw_to_en mapping to find splits
    raw_to_en = {}
    for j in range(n_en):
        for r in en_to_raw[j]:
            raw_to_en.setdefault(r, []).append(j)
            
    # Generate new IDs
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
                sub_idx = chunks.index(j)
                suffix = chr(ord('a') + sub_idx)
                new_ids[j] = f"P{r_first+1:03d}{suffix}"
        else:
            # Merged range (explicit as requested: P010_011)
            new_ids[j] = f"P{r_first+1:03d}_{r_last+1:03d}"
            
    # Print results
    for j in range(n_en):
        r_list = en_to_raw[j]
        r_str = ", ".join(f"R{r+1:03d}" for r in r_list)
        print(f"C{j+1:02d}: [{j+1:03d} -> {new_ids[j]}] | Maps to raw: {r_str} | Preview: {en_p[j][:60]}...")

if __name__ == '__main__':
    main()
