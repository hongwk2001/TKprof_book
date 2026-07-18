with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
    paragraphs = f.read().split("\n")

with open("scratch/ch24_indices.txt", "w", encoding="utf-8") as out:
    for i, p in enumerate(paragraphs):
        out.write(f"Index {i}: {p[:60]}\n")
