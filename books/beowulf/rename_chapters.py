import os
import re

roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}

def r2i(s):
    total = 0
    prev = 0
    for c in reversed(s):
        curr = roman_map.get(c, 0)
        total += curr if curr >= prev else -curr
        prev = curr
    return total

folder = r'D:\git_repo\TKprof_book\books\beowulf\chapters'
for f in os.listdir(folder):
    m = re.match(r'^Chapter_([IVXLCDM]+)(_en)?\.txt$', f)
    if m:
        roman = m.group(1)
        suffix = m.group(2) if m.group(2) else ''
        arabic = r2i(roman)
        new_name = f'Chapter_{arabic:02d}_{roman}{suffix}.txt'
        os.rename(os.path.join(folder, f), os.path.join(folder, new_name))
