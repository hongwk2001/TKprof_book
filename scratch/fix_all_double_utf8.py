import os
import glob

# CP1252 mapping dictionary from Windows-1252 byte to Unicode code point
cp1252_map = {
    0x80: 0x20AC, 0x82: 0x201A, 0x83: 0x0192, 0x84: 0x201E, 0x85: 0x2026,
    0x86: 0x2020, 0x87: 0x2021, 0x88: 0x02C6, 0x89: 0x2030, 0x8A: 0x0160,
    0x8B: 0x2039, 0x8C: 0x0152, 0x8E: 0x017D, 0x91: 0x2018, 0x92: 0x2019,
    0x93: 0x201C, 0x94: 0x201D, 0x95: 0x2022, 0x96: 0x2013, 0x97: 0x2014,
    0x98: 0x02DC, 0x99: 0x2122, 0x9A: 0x0161, 0x9B: 0x203A, 0x9C: 0x0153,
    0x9E: 0x017E, 0x9F: 0x0178
}
# Inverse map: Unicode code point to CP1252 byte value
unicode_to_byte = {v: k for k, v in cp1252_map.items()}

def recover_text(corrupted_text):
    if corrupted_text.startswith('\ufeff'):
        corrupted_text = corrupted_text[1:]
        
    byte_list = []
    for c in corrupted_text:
        val = ord(c)
        if val in unicode_to_byte:
            byte_list.append(unicode_to_byte[val])
        elif val < 256:
            byte_list.append(val)
        else:
            # Fallback for unexpected characters
            print(f"Warning: character {c} (U+{val:04X}) cannot be mapped, using placeholder")
            byte_list.append(ord('?'))
            
    raw_bytes = bytes(byte_list)
    return raw_bytes.decode('utf-8')

def fix_file(path):
    print(f"Fixing {os.path.basename(path)}...")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        
    # Check if double encoded (if it contains classic Mojibake characters)
    if "ë" in text or "ì" in text or "í" in text:
        try:
            fixed = recover_text(text)
            with open(path, "w", encoding="utf-8-sig") as out:
                out.write(fixed)
            print(f"  Successfully fixed!")
        except Exception as e:
            print(f"  Failed to fix: {e}")
    else:
        print("  Already seems clean (no double UTF-8 markers).")

def main():
    target_dir = r"d:\git_repo\TKprof_book\books\frankenstein\chapters"
    # Fix files in main chapters folder
    for path in glob.glob(os.path.join(target_dir, "*.txt")):
        fix_file(path)
    # Fix files in parts folder
    for path in glob.glob(os.path.join(target_dir, "parts", "*.txt")):
        fix_file(path)

if __name__ == "__main__":
    main()
