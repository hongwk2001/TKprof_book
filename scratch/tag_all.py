import os
import re

# Integrity Clean function
def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w]', '', text)
    return text.lower()

# Chapter 19 Tagging
def tag_ch_19():
    with open("books/odyssey/chapters/ch_19_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 34 quotes
    speakers = [
        "odysseus", "telemachus", "others", "telemachus", "telemachus",
        "odysseus", "others", "odysseus", "others", "others",
        "others", "odysseus", "others", "odysseus", "others",
        "odysseus", "others", "odysseus", "others", "odysseus",
        "others", "others", "odysseus", "others", "others",
        "others", "odysseus", "others", "odysseus", "others",
        "odysseus", "others", "odysseus", "others"
    ]
    
    parts = re.split(r'("[^"]*")', content)
    quote_idx = 0
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            tag = speakers[quote_idx]
            new_parts.append(f"<{tag}>{part}</{tag}>")
            quote_idx += 1
        else:
            new_parts.append(part)
            
    tagged = "".join(new_parts)
    assert clean_text(content) == clean_text(tagged), "Ch 19 Mismatch!"
    return tagged

# Chapter 20 Tagging (uses single quotes)
def tag_ch_20():
    with open("books/odyssey/chapters/ch_20_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    speakers = [
        "odysseus", "others", "odysseus", "odysseus", "others",
        "others", "odysseus", "others", "telemachus", "others",
        "others", "others", "odysseus", "others", "others",
        "others", "odysseus", "others", "others", "telemachus",
        "others", "others", "telemachus", "others", "telemachus",
        "others", "others", "others", "others"
    ]
    
    parts = re.split(r"('[^']*')", content)
    quote_idx = 0
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            tag = speakers[quote_idx]
            new_parts.append(f"<{tag}>{part}</{tag}>")
            quote_idx += 1
        else:
            new_parts.append(part)
            
    tagged = "".join(new_parts)
    assert clean_text(content) == clean_text(tagged), "Ch 20 Mismatch!"
    return tagged

# Chapter 21 Tagging
def tag_ch_21():
    with open("books/odyssey/chapters/ch_21_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    speakers = [
        "others", "others", "others", "telemachus", "telemachus",
        "telemachus", "others", "others", "others", "others",
        "others", "others", "odysseus", "odysseus", "others",
        "others", "odysseus", "odysseus", "odysseus", "others",
        "others", "odysseus", "others", "others", "others",
        "others", "telemachus", "others", "telemachus", "others",
        "others", "others", "odysseus"
    ]
    
    parts = re.split(r'("[^"]*")', content)
    quote_idx = 0
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            tag = speakers[quote_idx]
            new_parts.append(f"<{tag}>{part}</{tag}>")
            quote_idx += 1
        else:
            new_parts.append(part)
            
    tagged = "".join(new_parts)
    assert clean_text(content) == clean_text(tagged), "Ch 21 Mismatch!"
    return tagged

# Chapter 22 Tagging
def tag_ch_22():
    with open("books/odyssey/chapters/ch_22_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    speakers = [
        "odysseus", "others", "odysseus", "others", "odysseus",
        "others", "telemachus", "odysseus", "others", "others",
        "odysseus", "telemachus", "others", "odysseus", "others",
        "odysseus", "others", "others", "others", "odysseus",
        "others", "others", "odysseus", "others", "telemachus",
        "others", "odysseus", "odysseus", "telemachus", "odysseus",
        "others", "odysseus", "odysseus", "telemachus", "odysseus",
        "others", "odysseus"
    ]
    
    parts = re.split(r'("[^"]*")', content)
    quote_idx = 0
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            tag = speakers[quote_idx]
            new_parts.append(f"<{tag}>{part}</{tag}>")
            quote_idx += 1
        else:
            new_parts.append(part)
            
    tagged = "".join(new_parts)
    assert clean_text(content) == clean_text(tagged), "Ch 22 Mismatch!"
    return tagged

# Chapter 23 Tagging
def tag_ch_23():
    with open("books/odyssey/chapters/ch_23_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    speakers = [
        "others", "others", "others", "others", "others",
        "others", "others", "others", "others", "others",
        "others", "others", "others", "others", "others",
        "telemachus", "others", "odysseus", "telemachus", "odysseus",
        "others", "odysseus", "others", "odysseus", "others",
        "odysseus", "others", "odysseus", "others", "odysseus"
    ]
    
    parts = re.split(r'("[^"]*")', content)
    quote_idx = 0
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            tag = speakers[quote_idx]
            new_parts.append(f"<{tag}>{part}</{tag}>")
            quote_idx += 1
        else:
            new_parts.append(part)
            
    tagged = "".join(new_parts)
    assert clean_text(content) == clean_text(tagged), "Ch 23 Mismatch!"
    return tagged

# Chapter 24 Tagging
def tag_ch_24():
    with open("books/odyssey/chapters/ch_24_ko.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
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
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
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
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P48
        elif i == 48:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}<odysseus>"{parts[3]}"</odysseus>'
            
        # P50
        elif i == 50:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
            
        # P52
        elif i == 52:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P54
        elif i == 54:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}<odysseus>"{parts[3]}"</odysseus>'
            
        # P56
        elif i == 56:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P58
        elif i == 58:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
            
        # P60
        elif i == 60:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
            
        # P62
        elif i == 62:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P66
        elif i == 66:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P68
        elif i == 68:
            parts = p.split('"')
            paragraphs[i] = f'<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
            
        # P72
        elif i == 72:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P76
        elif i == 76:
            parts = p.split('"')
            paragraphs[i] = f'<others>"{parts[1]}"</others>{parts[2]}<others>"{parts[3]}"</others>'
            
        # P80
        elif i == 80:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P82
        elif i == 82:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P86
        elif i == 86:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}<others>"{parts[3]}"</others>{parts[4]}'
            
        # P90
        elif i == 90:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<odysseus>"{parts[1]}"</odysseus>{parts[2]}'
            
        # P92
        elif i == 92:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<telemachus>"{parts[1]}"</telemachus>{parts[2]}'
            
        # P94
        elif i == 94:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P96
        elif i == 96:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'
            
        # P100
        elif i == 100:
            parts = p.split('"')
            paragraphs[i] = f'{parts[0]}<others>"{parts[1]}"</others>{parts[2]}'

    tagged = "\n".join(paragraphs)
    assert clean_text(content) == clean_text(tagged), "Ch 24 Mismatch!"
    return tagged

def main():
    # Tag and save ch 19
    tagged_19 = tag_ch_19()
    with open("books/odyssey/chapters/tagged/tagged_ch_19_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_19)
    print("Chapter 19 tagged successfully!")
    
    # Tag and save ch 20
    tagged_20 = tag_ch_20()
    with open("books/odyssey/chapters/tagged/tagged_ch_20_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_20)
    print("Chapter 20 tagged successfully!")
    
    # Tag and save ch 21
    tagged_21 = tag_ch_21()
    with open("books/odyssey/chapters/tagged/tagged_ch_21_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_21)
    print("Chapter 21 tagged successfully!")
    
    # Tag and save ch 22
    tagged_22 = tag_ch_22()
    with open("books/odyssey/chapters/tagged/tagged_ch_22_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_22)
    print("Chapter 22 tagged successfully!")
    
    # Tag and save ch 23
    tagged_23 = tag_ch_23()
    with open("books/odyssey/chapters/tagged/tagged_ch_23_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_23)
    print("Chapter 23 tagged successfully!")
    
    # Tag and save ch 24
    tagged_24 = tag_ch_24()
    with open("books/odyssey/chapters/tagged/tagged_ch_24_ko.txt", "w", encoding="utf-8") as f:
        f.write(tagged_24)
    print("Chapter 24 tagged successfully!")

if __name__ == "__main__":
    main()
