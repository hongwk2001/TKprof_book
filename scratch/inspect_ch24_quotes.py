with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open("scratch/ch24_quotes_lines.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if '"' in line:
            out.write(f"Line {idx+1}: {line.strip()[:100]}\n")
