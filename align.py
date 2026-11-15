
import re

def get_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

en_text = open('books/dracula/chapters/ch27_en.txt', encoding='utf-8').read().strip()
ko_text = open('books/dracula/chapters/ch27_ko.txt', encoding='utf-8').read().strip()

en_paragraphs = en_text.split('\n\n')
ko_clean = re.sub(r'\[P\d{3}\]', '', ko_text).strip()
ko_clean = re.sub(r'\n+', ' ', ko_clean)

ko_sentences = get_sentences(ko_clean)

# We want exactly len(en_paragraphs) paragraphs.
assert len(en_paragraphs) == 135

en_lens = [len(p) for p in en_paragraphs]
tot_en = sum(en_lens)
en_cum = [sum(en_lens[:i]) / tot_en for i in range(136)]

ko_lens = [len(s) for s in ko_sentences]
tot_ko = sum(ko_lens)
ko_cum = [sum(ko_lens[:i]) / tot_ko for i in range(len(ko_sentences) + 1)]

ko_paras = [[] for _ in range(135)]
ko_idx = 0

for p_idx in range(135):
    en_end = en_cum[p_idx+1]
    # Keep adding sentences to current paragraph while their midpoint is <= en_end
    # or if we're forced to add at least something?
    # Wait, the prompt says 'Re-distribute all the sentences across all 135 Korean paragraphs'.
    while ko_idx < len(ko_sentences):
        midpoint = (ko_cum[ko_idx] + ko_cum[ko_idx+1]) / 2
        if midpoint <= en_end or p_idx == 134:
            ko_paras[p_idx].append(ko_sentences[ko_idx])
            ko_idx += 1
        else:
            break

# Ensure exactly 135 paragraphs
# Write out
out_text = '\n\n'.join([' '.join(sents) for sents in ko_paras])
with open('books/dracula/chapters/aligned_ko_ch27.txt', 'w', encoding='utf-8') as f:
    f.write(out_text)

print('Done! Paras:', len(ko_paras))

