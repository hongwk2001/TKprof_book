with open("d:/git_repo/TKprof_book/books/odyssey/chapters/ch_12_en.txt", "r", encoding="utf-8") as f:
    en_lines = f.readlines()

for i, line in enumerate(en_lines):
    clean = line.strip()
    status = "BLANK" if not clean else clean[:40]
    print(f"{i+1:02d}: {status}")
