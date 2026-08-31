import re

filename = 'books/dracula/chapters/ch13_en.txt'
with open(filename, 'r', encoding='utf-8') as f:
    text = f.read()

# For P086
old_p86 = "[P086]"
idx = text.find(old_p86)
if idx != -1:
    end_idx = text.find("\n[", idx + 1)
    if end_idx == -1: end_idx = len(text)
    para = text[idx:end_idx]
    
    split_str = "remain silent forever."
    split_idx = para.find(split_str)
    if split_idx != -1:
        split_idx += len(split_str)
        part1 = para[:split_idx].replace("[P086]", "[P086a]")
        part2 = para[split_idx:].strip()
        part2 = "[P086b] " + part2
        new_para = part1 + "\n" + part2
        text = text[:idx] + new_para + text[end_idx:]

# For P087
idx = text.find("[P087]")
if idx != -1:
    end_idx = text.find("\n[", idx + 1)
    if end_idx == -1: end_idx = len(text)
    para = text[idx:end_idx]
    
    split_str1 = "drained the color from my face."
    split_str2 = "heavy burdens.\""
    
    split_idx1 = para.find(split_str1)
    if split_idx1 != -1:
        split_idx1 += len(split_str1)
        part1 = para[:split_idx1].replace("[P087]", "[P087a]")
        
        rest = para[split_idx1:].strip()
        split_idx2 = rest.find(split_str2)
        if split_idx2 != -1:
            split_idx2 += len(split_str2)
            part2 = rest[:split_idx2]
            part3 = rest[split_idx2:].strip()
            
            part2 = "[P087b] " + part2
            part3 = "[P087c] " + part3
            new_para = part1 + "\n" + part2 + "\n" + part3
            text = text[:idx] + new_para + text[end_idx:]
        else:
            print("P087 split2 not found")
    else:
        print("P087 split1 not found")

# For P103
old_p103 = "[P103]"
idx = text.find(old_p103)
if idx != -1:
    end_idx = text.find("\n[", idx + 1)
    if end_idx == -1: end_idx = len(text)
    para = text[idx:end_idx]
    
    split_str = "morning in a cold state."
    split_idx = para.find(split_str)
    if split_idx != -1:
        split_idx += len(split_str)
        part1 = para[:split_idx].replace("[P103]", "[P103a]")
        part2 = para[split_idx:].strip()
        part2 = "[P103b] " + part2
        new_para = part1 + "\n" + part2
        text = text[:idx] + new_para + text[end_idx:]

with open(filename, 'w', encoding='utf-8') as f:
    f.write(text)
