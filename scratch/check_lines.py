with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"d:\git_repo\TKprof_book\scratch\check_lines_out.txt", "w", encoding="utf-8") as out:
    for i in range(25, 45):
        out.write(f"Line {i+1}: {repr(lines[i])}\n")
