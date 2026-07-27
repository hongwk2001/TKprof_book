path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_01_ko.txt"
with open(path, "rb") as f:
    raw_bytes = f.read()

print("First 150 bytes in hex:")
print(raw_bytes[:150].hex())

print("First 150 bytes as characters if decoded as latin-1:")
print(raw_bytes[:150].decode('latin-1'))
