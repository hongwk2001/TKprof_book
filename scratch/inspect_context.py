with open(r"d:\git_repo\TKprof_book\books\odyssey\chapters\ch_14_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

with open(r"d:\git_repo\TKprof_book\scratch\inspect_context_out.txt", "w", encoding="utf-8") as out:
    out.write("Context around 13800-14200:\n")
    out.write(repr(content[13800:14200]))
