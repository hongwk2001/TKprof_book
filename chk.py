import re

def get_tags(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return re.findall(r'\[(.*?)\]', content)

en = get_tags(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_en.txt')
ko = get_tags(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt')

print(f"EN tags: {len(en)}")
print(f"KO tags: {len(ko)}")
for i, (e, k) in enumerate(zip(en, ko)):
    if e != k:
        print(f"Mismatch at {i}: {e} != {k}")
        break
if len(en) != len(ko):
    print("Length mismatch")
