import re

with open('books/dracula/chapters/ch07_en.txt', 'r', encoding='utf-8') as f:
    en_text = f.read()
en_paras = [p.strip() for p in re.split(r'\[P\d+\]\s*', en_text)[1:]]

with open('books/dracula/chapters/ch07_ko.txt', 'r', encoding='utf-8') as f:
    ko_text = f.read()
ko_text = re.sub(r'\[P\d+\]\s*', '', ko_text)
ko_sentences = re.split(r'(?<=[.!?])\s+', ko_text.replace('\n', ' '))
ko_sentences = [s.strip() for s in ko_sentences if s.strip()]

en_lens = [len(p) for p in en_paras]
en_cum = [0]
for l in en_lens:
    en_cum.append(en_cum[-1] + max(1, l)) # avoid 0
    
ko_lens = [len(s) for s in ko_sentences]
ko_cum = [0]
for l in ko_lens:
    ko_cum.append(ko_cum[-1] + max(1, l))

total_en = en_cum[-1]
total_ko = ko_cum[-1]

chunks = [[] for _ in range(79)]
curr_p = 0

for i, s in enumerate(ko_sentences):
    # center of the sentence in terms of cumulative length
    s_center = ko_cum[i] + ko_lens[i] / 2
    
    # corresponding center in english
    expected_en_center = s_center / total_ko * total_en
    
    # find which english paragraph this center belongs to
    best_p = curr_p
    while best_p < 78 and en_cum[best_p + 1] < expected_en_center:
        best_p += 1
        
    chunks[best_p].append(s)

# However, some paragraphs might end up empty!
# We MUST ensure exactly 79 paragraphs, and ideally no empty ones.
# Let's fix empty paragraphs by stealing from neighbors.
for i in range(79):
    if not chunks[i]:
        # steal from previous or next
        if i > 0 and len(chunks[i-1]) > 1:
            chunks[i].append(chunks[i-1].pop())
        elif i < 78 and len(chunks[i+1]) > 1:
            chunks[i].append(chunks[i+1].pop(0))
        else:
            chunks[i].append(".") # fallback

# Write output
with open('books/dracula/chapters/aligned_ko_ch07.txt', 'w', encoding='utf-8') as f:
    for chunk in chunks:
        f.write(" ".join(chunk) + "\n\n")

