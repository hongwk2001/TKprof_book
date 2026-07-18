import re

def extract_ch_20():
    file_path = "books/odyssey/chapters/ch_20_ko.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # In chapter 20, quotes are single quotes `'`
    paragraphs = content.split("\n")
    print("=== Chapter 20 Quotes ===")
    
    quote_idx = 0
    with open("scratch/ch20_quotes.txt", "w", encoding="utf-8") as out:
        for p_idx, p in enumerate(paragraphs):
            if not p.strip():
                continue
            matches = list(re.finditer(r"'([^']*)'", p))
            if matches:
                out.write(f"Paragraph {p_idx}:\n")
                out.write(f"  Context: {p[:120]}...\n")
                for m in matches:
                    out.write(f"  [{quote_idx}] {m.group(0)}\n")
                    quote_idx += 1
                out.write("\n")

if __name__ == "__main__":
    extract_ch_20()
