import re

with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"d:\git_repo\TKprof_book\scratch\quotes_by_line.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        line_num = idx + 1
        quotes = re.findall(r'"[^"]*"', line)
        if quotes:
            out.write(f"Line {line_num}: {line.strip()}\n")
            for q in quotes:
                out.write(f"  -> {q}\n")
