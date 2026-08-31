import re

en = open('ch08_en.txt', encoding='utf-8').read().split('\n\n')
ko = open('ch08_ko.txt', encoding='utf-8').read().split('\n\n')

en_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p.strip()).group(1) for p in en if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p.strip())]
ko_tags = [re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p.strip()).group(1) for p in ko if re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p.strip())]

min_len = min(len(en_tags), len(ko_tags))

en_only_tags = en_tags[:min_len]
ko_only_tags = ko_tags[:min_len]

for i in range(min_len):
    if en_tags[i] != ko_tags[i]:
        print(f"Mismatch at index {i}: EN={en_tags[i]} KO={ko_tags[i]}")
        break

# Let's see what is at index of P047
idx = en_only_tags.index('P047')
print(f"Index {idx}")
print("EN Tag:", en_only_tags[idx])
print("KO Tag:", ko_only_tags[idx])

# Let's count sentences in EN index 75 and KO index 75
en_paras_raw = [p.strip() for p in en if p.strip()]
ko_paras_raw = [p.strip() for p in ko if p.strip()]

def count(p):
    text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
    return len(re.findall(r'[.!?](?:\s|\"|\”|\'|$)', text))

print(f"EN paras len: {len(en_paras_raw)}")
print(f"KO paras len: {len(ko_paras_raw)}")

print("EN count for P047:", count(en_paras_raw[idx]))
print("KO count for P047:", count(ko_paras_raw[idx]))

# Let's find out what paragraph the audit script actually processed for P047
en_paras_audit = []
for p in en_paras_raw:
    text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
    tag_match = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
    if tag_match:
        en_paras_audit.append({'tag': tag_match.group(1), 'text': text})

ko_paras_audit = []
for p in ko_paras_raw:
    text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
    tag_match = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
    if tag_match:
        ko_paras_audit.append({'tag': tag_match.group(1), 'text': text})

print("Audit EN tag at index 75:", en_paras_audit[75]['tag'])
print("Audit KO tag at index 75:", ko_paras_audit[75]['tag'])
print("Audit EN text count at index 75:", len(re.findall(r'[.!?](?:\s|\"|\”|\'|$)', en_paras_audit[75]['text'])))
