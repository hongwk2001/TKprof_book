import os
import re

ko_file = 'c:/git_repo/TKprof_book/books/dracula/chapters/ch25_ko.txt'

with open(ko_file, 'r', encoding='utf-8') as f:
    ko_text = f.read()

# We need to find the [P087da] block.
def repl(m):
    block = m.group(1)
    # find the first '! '
    return '[P087da]' + block.replace('! ', '!\n\n[P087db] ', 1)

ko_text = re.sub(r'\[P087da\](.*?)(?=\[P088\])', repl, ko_text, flags=re.DOTALL)

with open(ko_file, 'w', encoding='utf-8') as f:
    f.write(ko_text)

print("P087d final replacement done!")
