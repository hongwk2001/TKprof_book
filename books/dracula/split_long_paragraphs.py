import os
import re
import math

BASE_DIR = r'c:\git_repo\TKprof_book\books\dracula\chapters'
LIMIT = 100

def get_words(text):
    return len(text.split())

def split_sentences_en(text):
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z"“\'])', text)
    return [s.strip() for s in sents if s.strip()]

def split_sentences_ko(text):
    sents = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sents if s.strip()]

def strip_tags(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text)

def dp_align(en_sents, ko_sents):
    n_en = len(en_sents)
    n_ko = len(ko_sents)
    if n_en == 0 or n_ko == 0:
        return [(en_sents, ko_sents)]
        
    K = min(n_en, n_ko)
    en_buckets = [[] for _ in range(K)]
    for i in range(n_en):
        b = min(K - 1, math.floor(i * K / n_en))
        en_buckets[b].append(en_sents[i])
        
    ko_buckets = [[] for _ in range(K)]
    for i in range(n_ko):
        b = min(K - 1, math.floor(i * K / n_ko))
        ko_buckets[b].append(ko_sents[i])
        
    return [(en_buckets[b], ko_buckets[b]) for b in range(K)]

def group_chunks(chunks):
    final_chunks = []
    current_en = []
    current_ko = []
    
    for en_s, ko_s in chunks:
        candidate_en = current_en + en_s
        candidate_ko = current_ko + ko_s
        
        en_len = sum(get_words(s) for s in candidate_en)
        ko_len = sum(get_words(s) for s in candidate_ko)
        
        if (en_len > LIMIT or ko_len > LIMIT) and current_en:
            final_chunks.append((current_en, current_ko))
            current_en = en_s
            current_ko = ko_s
        else:
            current_en = candidate_en
            current_ko = candidate_ko
            
    if current_en or current_ko:
        final_chunks.append((current_en, current_ko))
        
    return final_chunks

def process_chapter(ch):
    en_path = os.path.join(BASE_DIR, f'ch{ch:02d}_en.txt')
    ko_path = os.path.join(BASE_DIR, f'ch{ch:02d}_ko.txt')
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
    with open(ko_path, 'r', encoding='utf-8') as f:
        ko_paras = [p.strip() for p in f.read().split('\n\n') if p.strip()]
        
    new_en_paras = []
    new_ko_paras = []
    
    modified = False
    
    for ep, kp in zip(en_paras, ko_paras):
        tag_match = re.match(r'^(\[P[0-9a-zA-Z_]+\])\s*', ep)
        tag = tag_match.group(1) if tag_match else "[Pxxx]"
        
        clean_en = strip_tags(ep)
        clean_ko = strip_tags(kp)
        
        en_w = get_words(clean_en)
        ko_w = get_words(clean_ko)
        
        if en_w > LIMIT or ko_w > LIMIT:
            modified = True
            en_sents = split_sentences_en(clean_en)
            ko_sents = split_sentences_ko(clean_ko)
            
            if not en_sents: en_sents = [clean_en]
            if not ko_sents: ko_sents = [clean_ko]
            
            chunks = dp_align(en_sents, ko_sents)
            grouped = group_chunks(chunks)
            
            for gen, gko in grouped:
                new_en_paras.append(tag + ' ' + ' '.join(gen))
                new_ko_paras.append(tag + ' ' + ' '.join(gko))
        else:
            new_en_paras.append(ep)
            new_ko_paras.append(kp)
            
    if modified:
        with open(en_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_en_paras))
        with open(ko_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_ko_paras))
        print(f"Ch {ch:02d}: Split long paragraphs.")
        return True
    return False

def main():
    for i in range(1, 28):
        process_chapter(i)
    print("Done splitting all chapters.")

if __name__ == '__main__':
    main()
