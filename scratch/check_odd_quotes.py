with open("scratch/odd_quotes_results.txt", "w", encoding="utf-8") as out:
    for ch in range(19, 25):
        path = f"books/odyssey/chapters/ch_{ch}_ko.txt"
        with open(path, "r", encoding="utf-8") as f:
            paragraphs = f.read().split("\n")
        
        quote_char = "'" if ch == 20 else '"'
        for p_idx, p in enumerate(paragraphs):
            count = p.count(quote_char)
            if count % 2 != 0:
                out.write(f"Chapter {ch}, Paragraph {p_idx}: odd count ({count}) of {quote_char}\n")
                out.write(f"  Text: {p[:120]}...\n\n")
