with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"d:\git_repo\TKprof_book\scratch\inspect_lines_58_72.txt", "w", encoding="utf-8") as out:
    for idx in range(57, 72):
        out.write(f"Line {idx+1}: {repr(lines[idx])}\n")
