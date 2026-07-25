import os
import re
import sys

# Reconfigure stdout to print UTF-8 characters safely on Windows console
sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"d:\git_repo\TKprof_book\books\scaramouche\chapters"

print("Scanning Scaramouche files for non-English bleed-through and Korean encoding issues...")

found_bleed = False
found_ko_artifacts = False

# Regular expression to match Korean Hangul characters
hangul_re = re.compile(r"[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f\ua960-\ua97f\ud7b0-\ud7ff]")

for root, dirs, files in os.walk(base_dir):
    for f in files:
        path = os.path.join(root, f)
        
        # 1. Check if English files contain Korean characters (bleed-through)
        if f.endswith("_en.txt") or f == "introduction_en.txt" or f == "copyright_en.txt":
            try:
                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()
                matches = hangul_re.findall(content)
                if matches:
                    print(f"Bleed-through: Found Korean characters in English file {f}: {set(matches)}")
                    found_bleed = True
            except Exception as e:
                print(f"Error reading {f}: {e}")
                
        # 2. Check if Korean files contain bad decodings/corrupted symbols
        elif f.endswith("_ko.txt") or f == "introduction_ko.txt" or f == "copyright_ko.txt":
            try:
                with open(path, "r", encoding="utf-8") as file:
                    lines = file.readlines()
                for line_idx, line in enumerate(lines, 1):
                    for char in line:
                        o = ord(char)
                        if o > 127:
                            # Typical allowed range for Korean: hangul, standard punctuation, common accents, etc.
                            # Standard Hangul range is AC00-D7A3, compatibility jamo is 3130-318F.
                            # Also allow standard smart quotes (2018, 2019, 201c, 201d), em-dash (2014), en-dash (2013), mid-dot (00b7)
                            # Allow French accents if they appear in names: e.g. é (00e9)
                            if (0xac00 <= o <= 0xd7a3) or (0x3130 <= o <= 0x318f) or o in [
                                0x2013, 0x2014, 0x2018, 0x2019, 0x201c, 0x201d, 0x00e9, 0x00e0, 0x00e8, 0x00e2, 
                                0x00fb, 0x00ee, 0x00f4, 0x00e7, 0x00ef, 0x00c9, 0x00c0, 0x00b7, 0xff0c, 0x3002,
                                0x3001, 0x300c, 0x300d, 0x300e, 0x300f, 0x300a, 0x300b, 0x2026, 0x201c, 0x201d
                            ]:
                                continue
                            print(f"Suspect char in Korean file {f} line {line_idx}: {char!r} (U+{o:04X}) in context: {line.strip()}")
                            found_ko_artifacts = True
            except Exception as e:
                print(f"Error reading {f}: {e}")

if not found_bleed:
    print("Clean: No Korean bleed-through found in English files.")
if not found_ko_artifacts:
    print("Clean: No suspicious encoding characters found in Korean files.")
