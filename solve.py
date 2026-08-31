import re
import urllib.request, urllib.parse, json
import difflib

def translate(text):
    if not text.strip(): return ""
    try:
        url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=ko&dt=t&q=' + urllib.parse.quote(text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        data = json.loads(response.read().decode('utf-8'))
        return ''.join([x[0] for x in data[0]])
    except:
        return ""

# Read English
with open('books/dracula/chapters/ch07_en.txt', 'r', encoding='utf-8') as f:
    en_text = f.read()
en_paras = [p.strip() for p in re.split(r'\[P\d+\]\s*', en_text)[1:]]

# Read Korean
with open('books/dracula/chapters/ch07_ko.txt', 'r', encoding='utf-8') as f:
    ko_text = f.read()
ko_text = re.sub(r'\[P\d+\]\s*', '', ko_text).strip()
ko_sentences = re.split(r'(?<=[.!?])\s+', ko_text.replace('\n', ' '))

# Translate English paras
en_trans = []
for i, p in enumerate(en_paras):
    en_trans.append(translate(p))

# Align
aligned_ko = []
start_idx = 0

for i, trans in enumerate(en_trans):
    if not trans:
        aligned_ko.append("")
        continue
        
    best_match_idx = start_idx
    best_score = 0
    best_end_idx = start_idx + 1
    
    # search for the best block of sentences
    for end_idx in range(start_idx + 1, min(start_idx + 25, len(ko_sentences) + 1)):
        block = " ".join(ko_sentences[start_idx:end_idx])
        sm = difflib.SequenceMatcher(None, trans, block)
        score = sm.ratio()
        if score > best_score:
            best_score = score
            best_end_idx = end_idx
            
    # Add block
    aligned_ko.append(" ".join(ko_sentences[start_idx:best_end_idx]))
    start_idx = best_end_idx

# Write output
with open('books/dracula/chapters/aligned_ko_ch07.txt', 'w', encoding='utf-8') as f:
    f.write("\n\n".join(aligned_ko))

print("Done")
