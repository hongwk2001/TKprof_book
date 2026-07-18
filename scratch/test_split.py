import re

with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
    paragraphs = f.read().split("\n")

p = paragraphs[12]
parts = re.split(r'("[^"]*")', p)

with open("scratch/test_split_out.txt", "w", encoding="utf-8") as out:
    out.write(f"Paragraph 12: {repr(p)}\n")
    out.write(f"Parts: {repr(parts)}\n")
