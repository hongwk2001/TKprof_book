import os
import json
import re
import glob

def parse_paragraphs(text, is_raw=False):
    if is_raw:
        text = text.replace('\r\n', '\n')
        paragraphs = re.split(r'\n\s*\n', text)
        cleaned_paragraphs = []
        for p in paragraphs:
            cleaned_p = re.sub(r'(?<!\n)\n(?!\n)', ' ', p)
            cleaned_p = cleaned_p.strip()
            if cleaned_p:
                cleaned_paragraphs.append(cleaned_p)
        return cleaned_paragraphs
    else:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        return paragraphs

def split_sentences(text):
    sentences = re.split(r'(?<!\bMr)(?<!\bMrs)(?<!\bMs)(?<!\bDr)(?<!\bSt)(?<!\bProf)(?<!\bRev)(?<=[.!?])\s+(?=[A-Z"\'\[])', text)
    return [s.strip() for s in sentences if s.strip()]

def align_dp(src_items, tgt_items):
    N = len(src_items)
    M = len(tgt_items)
    
    if N == 0 and M == 0:
        return []
    if N == 0:
        return [('', ' '.join(tgt_items))]
    if M == 0:
        return [(' '.join(src_items), '')]
    
    dp = [[float('inf')] * (M + 1) for _ in range(N + 1)]
    dp[0][0] = 0
    backtrack = [[None] * (M + 1) for _ in range(N + 1)]
    
    src_len = [len(x) for x in src_items]
    tgt_len = [len(x) for x in tgt_items]
    
    total_src = sum(src_len) + 1
    total_tgt = sum(tgt_len) + 1
    ratio = total_tgt / total_src
    
    max_chunk = 5 # allow up to 5 sentences to combine
    
    for i in range(N + 1):
        for j in range(M + 1):
            if dp[i][j] == float('inf'):
                continue
                
            for di in range(1, max_chunk + 1):
                for dj in range(1, max_chunk + 1):
                    if i + di <= N and j + dj <= M:
                        len_s = sum(src_len[i:i+di])
                        len_t = sum(tgt_len[j:j+dj])
                        
                        expected_t = len_s * ratio
                        diff_cost = abs(len_t - expected_t)
                        chunk_penalty = (di - 1) * 200 + (dj - 1) * 200
                        
                        cost = dp[i][j] + diff_cost + chunk_penalty
                        
                        if cost < dp[i+di][j+dj]:
                            dp[i+di][j+dj] = cost
                            backtrack[i+di][j+dj] = (i, j)
                            
    i, j = N, M
    aligned = []
    
    if dp[N][M] == float('inf'):
        print("DP Failed, falling back to proportional bucketing")
        return bucket_align(src_items, tgt_items)
        
    while i > 0 or j > 0:
        prev_i, prev_j = backtrack[i][j]
        src_chunk = src_items[prev_i:i]
        tgt_chunk = tgt_items[prev_j:j]
        aligned.append((' '.join(src_chunk), ' '.join(tgt_chunk)))
        i, j = prev_i, prev_j
        
    return aligned[::-1]

def bucket_align(src_items, tgt_items):
    aligned = []
    N = len(src_items)
    M = len(tgt_items)
    
    if N == 0 or M == 0:
        return [(' '.join(src_items), ' '.join(tgt_items))]
        
    for i, src in enumerate(src_items):
        start_idx = int(i * M / N)
        end_idx = int((i + 1) * M / N)
        if end_idx == start_idx:
            end_idx = start_idx + 1
        
        tgt = ' '.join(tgt_items[start_idx:end_idx])
        aligned.append((src, tgt))
    return aligned

def process_file(raw_path, mod_path, out_path):
    print(f"Processing {raw_path}...")
    with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
        raw_text = f.read()
    with open(mod_path, 'r', encoding='utf-8', errors='ignore') as f:
        mod_text = f.read()
        
    raw_paras = parse_paragraphs(raw_text, is_raw=True)
    mod_paras = parse_paragraphs(mod_text, is_raw=False)
    
    para_aligned = align_dp(raw_paras, mod_paras)
    
    json_data = []
    item_id = 1
    
    for p_idx, (r_para, m_para) in enumerate(para_aligned):
        r_sents = split_sentences(r_para)
        m_sents = split_sentences(m_para)
        
        if not r_sents and not m_sents:
            continue
            
        sent_aligned = align_dp(r_sents, m_sents)
        
        is_header = False
        if len(r_para) < 200 and ('chapter' in r_para.lower() or 'book ' in r_para.lower() or 'period' in r_para.lower()):
            is_header = True
            
        for s_idx, (r_s, m_s) in enumerate(sent_aligned):
            tag_base = f"P{p_idx+1:03d}"
            if len(sent_aligned) > 1:
                tag = f"{tag_base}_{s_idx+1}"
            else:
                tag = tag_base
                
            json_data.append({
                "id": item_id,
                "tag": tag,
                "raw": r_s,
                "en": m_s,
                "ko": "",
                "is_header": is_header
            })
            item_id += 1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

def main():
    raw_files = glob.glob('c:/git_repo/TKprof_book/books/two_cities/chapters/raw_*.txt')
    for raw_path in raw_files:
        basename = os.path.basename(raw_path)
        match = re.search(r'raw_(book\d+_ch_\d+)\.txt', basename)
        if match:
            book_ch = match.group(1)
            mod_path = f'c:/git_repo/TKprof_book/books/two_cities/chapters/{book_ch}_en.txt'
            out_path = f'c:/git_repo/TKprof_book/books/two_cities/json/{book_ch}.json'
            
            if os.path.exists(mod_path):
                process_file(raw_path, mod_path, out_path)
            else:
                print(f"Warning: Missing mod file for {raw_path}")

if __name__ == '__main__':
    main()
