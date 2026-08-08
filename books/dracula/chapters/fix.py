import re
input_path = r'c:\git_repo\TKprof_book\books\dracula\chapters\raw_ch_14.txt'
out_en_path = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch14_en.txt'
with open(input_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\u201c', '\"').replace('\u201d', '\"').replace('\u2019', '\'').replace('\u2018', '\'')

lines = text.split('\n')

paragraphs = []
current_para = []

for line in lines:
    line = line.strip()
    if not line:
        if current_para:
            paragraphs.append(' '.join(current_para))
            current_para = []
    else:
        current_para.append(line)

if current_para:
    paragraphs.append(' '.join(current_para))

cleaned_paras = []
for p in paragraphs:
    p = re.sub(r'\s+', ' ', p)
    cleaned_paras.append(p)

with open(out_en_path, 'w', encoding='utf-8') as f:
    for p in cleaned_paras:
        f.write(p + '\n')
print(f'Wrote {len(cleaned_paras)} paragraphs to {out_en_path}')
