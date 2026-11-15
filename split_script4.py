import re

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt'

with open(ko_file, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'(\[P082_083a\])(.*?)(?=\n\s*\[|$)'
match = re.search(pattern, content, re.DOTALL)
if match:
    para_text = match.group(2)
    split_str = '반 헬싱 교수님과 나는'
    if split_str in para_text:
        new_para_text = para_text.replace(split_str, '\n\n[P082_083b] ' + split_str, 1)
        new_content = content[:match.start(2)] + new_para_text + content[match.end(2):]
        with open(ko_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully fixed P082_083 in ko")
    else:
        print("Still didn't find the exact string")
else:
    print("Not found")
