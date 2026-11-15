import re
from googletrans import Translator

def align():
    with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_27.txt', 'r', encoding='utf-8') as f:
        en_text = f.read()

    paras = en_text.split('\n\n')
    en_sents = []
    for i, p in enumerate(paras):
        p = p.strip()
        if not p: continue
        # Split but keep the sentence strings together with their paragraph index
        sents = re.split(r'(?<=[.!?])\s+(?=[A-Z“_])', p.replace('\n', ' '))
        for s in sents:
            en_sents.append((i, s))

    with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt', 'r', encoding='utf-8') as f:
        ko_text = f.read()
    ko_paras = [p.strip() for p in ko_text.split('\n') if p.strip()]

    translator = Translator()
    ko_translated = []
    for kp in ko_paras:
        # Translate just the first 50 chars to get an idea
        t = translator.translate(kp[:50], src='ko', dest='en').text
        ko_translated.append(t)

    with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\trans_check.txt', 'w', encoding='utf-8') as f:
        for i, t in enumerate(ko_translated):
            f.write(f'KO {i}: {t}\n')

if __name__ == "__main__":
    align()
