import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch26_ko.txt'
with open(ko_file, 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'\[P082_083a\](.*?)\[P083b\]', content, re.DOTALL)
if match:
    idx = match.group(1).find("반 헬싱")
    if idx != -1:
        text_snippet = match.group(1)[idx:idx+100]
        # just write to a file, then we can read it easily
        with open('snippet.txt', 'w', encoding='utf-8') as f2:
            f2.write(text_snippet)
