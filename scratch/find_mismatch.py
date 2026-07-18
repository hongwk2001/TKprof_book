import re

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w]', '', text)
    return text.lower()

with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's import tag_ch_24 logic but without assertion
def tag_ch_24_no_assert():
    paragraphs = content.split("\n")
    for i, p in enumerate(paragraphs):
        if not p.strip():
            continue
            
        # P12
        if i == 12:
            parts = p.split('"')
            paragraphs[i] = f'<others>"{parts[1]}"</others>{parts[2]}<others>"{parts[3]}"</others>'
        # P14
        elif i == 14:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}</others>'
        # P16 (no quotes)
        elif i == 16:
            paragraphs[i] = f"<others>{p}</others>"
        # P18
        elif i == 18:
            paragraphs[i] = f"<others>{p}</others>"
        # P20 (no quotes)
        elif i == 20:
            paragraphs[i] = f"<others>{p}</others>"
        # P22 (no quotes)
        elif i == 22:
            paragraphs[i] = f"<others>{p}</others>"
        # P24
        elif i == 24:
            paragraphs[i] = f"<others>{p}</others>"
        # P26
        elif i == 26:
            paragraphs[i] = f"<others>{p[:-1]}</others>\""
        # P30
        elif i == 30:
            parts = p.split('"')
            paragraphs[i] = f'<others>"{parts[1]}"</others>{parts[2]}<others>"{parts[3]}"</others>'
        # P32
        elif i == 32:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}</others>'
        # P34
        elif i == 34:
            paragraphs[i] = f"<others>{p}</others>"
        # P36
        elif i == 36:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P40
        elif i == 40:
            paragraphs[i] = f"<odysseus>{p}</odysseus>"
        # P44
        elif i == 44:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}<odysseus>"{parts[3]}"</odysseus>'
        # P46
        elif i == 46:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P48
        elif i == 48:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}<odysseus>"{parts[3]}"</odysseus>'
        # P50
        elif i == 50:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>'
        # P52
        elif i == 52:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P54
        elif i == 54:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}<odysseus>"{parts[3]}"</odysseus>'
        # P56
        elif i == 56:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P58
        elif i == 58:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>'
        # P60
        elif i == 60:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
        # P62
        elif i == 62:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P66
        elif i == 66:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P68
        elif i == 68:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
        # P72
        elif i == 72:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P76
        elif i == 76:
            parts = p.split('"')
            paragraphs[i] = f'<others>"{parts[1]}"</others>{parts[2]}<others>"{parts[3]}"</others>'
        # P80
        elif i == 80:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P82
        elif i == 82:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P86
        elif i == 86:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>'
        # P90
        elif i == 90:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>'
        # P92
        elif i == 92:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<telemachus>"{parts[1]}"</telemachus>'
        # P94
        elif i == 94:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P96
        elif i == 96:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'
        # P100
        elif i == 100:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>'

    return "\n".join(paragraphs)

tagged = tag_ch_24_no_assert()
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
