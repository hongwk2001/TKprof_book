import re
import os

def extract_quotes(file_path, out_f):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    paragraphs = content.split("\n")
    out_f.write(f"=== Quotes in {os.path.basename(file_path)} ===\n")
    
    quote_idx = 0
    for p_idx, p in enumerate(paragraphs):
        if not p.strip():
            continue
        matches = list(re.finditer(r'("[^"]*"|“[^”]*”)', p))
        if matches:
            out_f.write(f"Paragraph {p_idx}:\n")
            out_f.write(f"  Context: {p[:150]}...\n")
            for m in matches:
                out_f.write(f"  [{quote_idx}] {m.group(0)}\n")
                quote_idx += 1
            out_f.write("\n")

if __name__ == "__main__":
    with open("scratch/quotes_info.txt", "w", encoding="utf-8") as out_f:
        for ch in range(19, 25):
            extract_quotes(f"books/odyssey/chapters/ch_{ch}_ko.txt", out_f)
