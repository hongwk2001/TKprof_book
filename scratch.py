import json

en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_en.txt'
ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt'

with open(en_file, 'r', encoding='utf-8') as f:
    en_lines = f.readlines()
with open(ko_file, 'r', encoding='utf-8') as f:
    ko_lines = f.readlines()

def get_para(lines, tag):
    for line in lines:
        if line.startswith(f"[{tag}]"):
            return line.strip()
    return None

tags = ['P003', 'P017', 'P027_028', 'P073d', 'P079d']
out = {}
for tag in tags:
    out[tag] = {
        'en': get_para(en_lines, tag),
        'ko': get_para(ko_lines, tag)
    }

with open(r'c:\git_repo\TKprof_book\scratch_out.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
