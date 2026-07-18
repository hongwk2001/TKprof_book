with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.findall(r'"[^"]*"', content)

with open(r"d:\git_repo\TKprof_book\scratch\dialogues_utf8.txt", "w", encoding="utf-8") as out:
    out.write(f"Total dialogues: {len(matches)}\n")
    for idx, match in enumerate(matches):
        out.write(f"{idx+1}: {match}\n")
