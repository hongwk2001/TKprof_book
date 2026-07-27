import os

path = r"d:\git_repo\TKprof_book\books\frankenstein\chapters\ch_01_ko.txt"
with open(path, "r", encoding="utf-8") as f:
    corrupted_text = f.read()

# Strip BOM if present
if corrupted_text.startswith('\ufeff'):
    corrupted_text = corrupted_text[1:]

try:
    # Try using cp1252 to encode back to original bytes
    fixed_bytes = corrupted_text.encode('cp1252')
    fixed_text = fixed_bytes.decode('utf-8')
    
    print("Recovery successful!")
    print("First 200 characters of recovered text:")
    print(repr(fixed_text[:200]))
    
    # Save the fixed file
    with open(path, "w", encoding="utf-8-sig") as out:
        out.write(fixed_text)
    print("Fixed file saved to:", path)
except Exception as e:
    print("Recovery failed:", e)
