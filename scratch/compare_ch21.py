import re

def clean(text):
    text = re.sub(r'\[P\d+\]\s*', '', text)
    return ' '.join(text.split())

def paras(p):
    with open(p, 'r', encoding='utf-8') as f:
        return [clean(x) for x in f.read().split('\n\n') if x.strip()]

raw_p = paras('books/dracula/chapters_backup/raw_ch_21.txt')
chunk_p = paras('books/dracula/chapters/ch21_en.txt')

print(f"Raw count: {len(raw_p)}, Chunked count: {len(chunk_p)}")

# Print them side by side
# Since Raw is 69 and Chunked is 64, let's list them sequentially and try to manually align or see where they diverge
r_idx = 0
c_idx = 0
while r_idx < len(raw_p) or c_idx < len(chunk_p):
    r_text = raw_p[r_idx] if r_idx < len(raw_p) else "[END]"
    c_text = chunk_p[c_idx] if c_idx < len(chunk_p) else "[END]"
    
    print(f"\n--- index R:{r_idx+1:02d} / C:{c_idx+1:02d} ---")
    print(f"Raw: {r_text[:140]}")
    print(f"Chn: {c_text[:140]}")
    
    # Just advance both for now
    r_idx += 1
    c_idx += 1
    if r_idx >= 15:
        break
