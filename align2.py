
import re

def get_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

en_text = open('books/dracula/chapters/ch27_en.txt', encoding='utf-8').read().strip()
ko_text = open('books/dracula/chapters/ch27_ko.txt', encoding='utf-8').read().strip()

en_paragraphs = en_text.split('\n\n')
ko_clean = re.sub(r'\[P\d{3}\]', '', ko_text).strip()
ko_clean = re.sub(r'\n+', ' ', ko_clean)

ko_sentences = get_sentences(ko_clean)

en_lens = [len(p) for p in en_paragraphs]
tot_en = sum(en_lens)

ko_paras = [[] for _ in range(135)]
ko_idx = 0

# Distribute sentences such that each gets at least 1
for p_idx in range(135):
    # Base assignment: at least 1 sentence
    ko_paras[p_idx].append(ko_sentences[ko_idx])
    ko_idx += 1
    
    # Target length for this paragraph based on characters
    target_len = en_lens[p_idx] / tot_en * sum(len(s) for s in ko_sentences)
    current_len = len(ko_paras[p_idx][0])
    
    while ko_idx < len(ko_sentences) - (134 - p_idx):
        if current_len + len(ko_sentences[ko_idx])/2 <= target_len or (p_idx == 134 and ko_idx < len(ko_sentences)):
            ko_paras[p_idx].append(ko_sentences[ko_idx])
            current_len += len(ko_sentences[ko_idx])
            ko_idx += 1
        else:
            break

# Ensure all remaining sentences go to the last paragraph
while ko_idx < len(ko_sentences):
    ko_paras[134].append(ko_sentences[ko_idx])
    ko_idx += 1

out_text = '\n\n'.join([' '.join(sents).strip() for sents in ko_paras])
with open('books/dracula/chapters/aligned_ko_ch27.txt', 'w', encoding='utf-8') as f:
    f.write(out_text)


