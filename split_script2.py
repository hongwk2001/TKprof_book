import re

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt'

with open(ko_file, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(\[P082_083\])(.*?)(?=\n\s*\[|$)'
match = re.search(pattern, content, re.DOTALL)
if match:
    para_text = match.group(2)
    split_norm = '반 헬싱 교수님과 저는'
    split_regex = re.escape(split_norm).replace(r'\ ', r'\s+')
    
    def repl(m):
        return '\n\n[P082_083b] ' + m.group(0).lstrip()

    new_para_text = re.sub(split_regex, repl, para_text, count=1)
    new_para = f"[P082_083a]{new_para_text}"
    new_content = content[:match.start()] + new_para + content[match.end():]
    with open(ko_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully split P082_083 in ko")
else:
    print("Not found")

