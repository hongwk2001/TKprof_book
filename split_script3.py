import re

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt'

with open(ko_file, 'r', encoding='utf-8') as f:
    content = f.read()

# I messed up P082_083a. It should be P082_083 in the regex now, but it's P082_083a in the file.
pattern = r'(\[P082_083a\])(.*?)(?=\n\s*\[|$)'
match = re.search(pattern, content, re.DOTALL)
if match:
    para_text = match.group(2)
    # let's just find the exact text using replace
    # "반 헬싱 교수님과 저는 오늘 밤"
    split_str = '반 헬싱 교수님과 저는'
    if split_str in para_text:
        new_para_text = para_text.replace(split_str, '\n\n[P082_083b] ' + split_str, 1)
        new_para = f"[P082_083a]{new_para_text}"
        new_content = content[:match.start()] + new_para + content[match.end():]
        with open(ko_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully fixed P082_083 in ko")
    else:
        print("Still didn't find the exact string")
else:
    print("Not found")

