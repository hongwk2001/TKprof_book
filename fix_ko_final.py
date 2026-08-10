import re

filename = 'books/dracula/chapters/ch13_ko.txt'
with open(filename, 'r', encoding='utf-8') as f:
    text = f.read()

# For P086
old_p86 = "[P086]"
idx = text.find(old_p86)
if idx != -1:
    end_idx = text.find("\n[", idx + 1)
    if end_idx == -1: end_idx = len(text)
    para = text[idx:end_idx]
    
    split_str = "영원히 침묵할 것이다."
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
    
    split_str = "처참한 순간에 말이야."
    split_idx = para.find(split_str)
    if split_idx != -1:
        split_idx += len(split_str)
        part1 = para[:split_idx].replace("[P087]", "[P087a]")
        part2 = para[split_idx:].strip()
        part2 = "[P087b] " + part2
        new_para = part1 + "\n" + part2
        text = text[:idx] + new_para + text[end_idx:]

# For P103
old_p103 = "[P103]"
idx = text.find(old_p103)
if idx != -1:
    end_idx = text.find("\n[", idx + 1)
    if end_idx == -1: end_idx = len(text)
    para = text[idx:end_idx]
    
    split_str = "상태로 발견되었다."
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
