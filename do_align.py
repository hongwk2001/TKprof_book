import json, re

with open('temp_out.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def split_sentences(text):
    text = text.replace('Dr.', 'Dr_dot').replace('Mr.', 'Mr_dot').replace('Mrs.', 'Mrs_dot')
    sentences = re.split(r'(?<=[.?!])\s+(?=[\"\'A-Z])', text)
    return [s.replace('Dr_dot', 'Dr.').replace('Mr_dot', 'Mr.').replace('Mrs_dot', 'Mrs.') for s in sentences]

def split_ko_sentences(text):
    sentences = re.split(r'(?<=[.?!])\s+(?=[\"\'?-?])', text)
    return sentences

with open('ch25_align.txt', 'w', encoding='utf-8') as f:
    for pid in ['P061', 'P078', 'P087d']:
        en_sents = split_sentences(data['en'][pid])
        ko_sents = split_ko_sentences(data['ko'][pid])
        f.write(f'=== {pid} ===\n')
        f.write(f'EN: {len(en_sents)} sentences\n')
        f.write(f'KO: {len(ko_sents)} sentences\n')
        max_len = max(len(en_sents), len(ko_sents))
        for i in range(max_len):
            e = en_sents[i] if i < len(en_sents) else ''
            k = ko_sents[i] if i < len(ko_sents) else ''
            f.write(f'[{i}] EN: {e}\n')
            f.write(f'[{i}] KO: {k}\n')
            f.write('-'*40 + '\n')
