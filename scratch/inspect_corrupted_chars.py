path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_01_ko.txt"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

large_chars = set()
for c in text:
    if ord(c) > 255:
        large_chars.add(c)

print("Characters > 255 in the corrupted file:")
for c in sorted(large_chars):
    print(f"Char: {c} | Code: U+{ord(c):04X} | Name: {c.encode('ascii', 'ignore')}")
