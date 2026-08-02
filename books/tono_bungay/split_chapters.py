import os
import re

def split_tono_bungay():
    raw_path = os.path.join(os.path.dirname(__file__), "tono_bungay_raw.txt")
    with open(raw_path, "r", encoding="utf-8") as f:
        text = f.read()

    end_offset = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    if end_offset != -1:
        text = text[:end_offset]

    # Chapter boundaries list: (book_num, ch_num, start_offset)
    chapters_info = [
        (1, 1, 1364),
        (1, 2, 75978),
        (1, 3, 122399),
        (2, 1, 182672),
        (2, 2, 243374),
        (2, 3, 281478),
        (2, 4, 307713),
        (3, 1, 399458),
        (3, 2, 447860),
        (3, 3, 538524),
        (3, 4, 606325),
        (4, 1, 669358),
        (4, 2, 727228),
        (4, 3, 750109),
    ]

    base_dir = os.path.join(os.path.dirname(__file__), "chapters")
    os.makedirs(base_dir, exist_ok=True)

    for i, (b_num, c_num, start_pos) in enumerate(chapters_info):
        if i + 1 < len(chapters_info):
            # End before next chapter starts (or book header before next chapter)
            next_start = chapters_info[i + 1][2]
            slice_text = text[start_pos:next_start]
            book_hdr_match = re.search(r'\n\s*BOOK THE [A-Z]+\s*\n', slice_text)
            if book_hdr_match:
                end_pos = start_pos + book_hdr_match.start()
            else:
                end_pos = next_start
        else:
            end_pos = len(text)

        ch_text = text[start_pos:end_pos].strip()

        book_dir = os.path.join(base_dir, f"book{b_num}")
        os.makedirs(book_dir, exist_ok=True)

        filename = f"book{b_num}_ch{c_num:02d}_en_raw.txt"
        filepath = os.path.join(book_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(ch_text)

        word_count = len(ch_text.split())
        print(f"Created {filepath} ({len(ch_text)} chars, {word_count} words)")

if __name__ == "__main__":
    split_tono_bungay()
