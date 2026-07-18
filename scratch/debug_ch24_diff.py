import sys
sys.path.append("scratch")
from tag_all import tag_ch_24, clean_text
import difflib

with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

tagged = tag_ch_24()

c1 = clean_text(content)
c2 = clean_text(tagged)

print("Len c1:", len(c1))
print("Len c2:", len(c2))

with open("scratch/diff_report.txt", "w", encoding="utf-8") as out:
    if c1 != c2:
        out.write("Mismatch at index:\n")
        for idx, (char1, char2) in enumerate(zip(c1, c2)):
            if char1 != char2:
                out.write(f"Diff at cleaned index {idx}: original={repr(char1)}, tagged={repr(char2)}\n")
                out.write(f"Context original: {c1[max(0, idx-40):idx+40]}\n")
                out.write(f"Context tagged:   {c2[max(0, idx-40):idx+40]}\n")
                break
    else:
        out.write("No mismatch found!\n")
