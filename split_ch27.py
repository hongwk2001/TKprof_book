import re

def split_text(text, split_marker, tag_base, part_a, part_b):
    # original pattern: [tag_base] ...
    # we want to replace with: [part_a] ... \n\n[part_b] ...
    para = ""
    start_idx = -1
    for i, line in enumerate(text):
        if line.startswith(f"[{tag_base}]"):
            para = line
            start_idx = i
            break
            
    if start_idx == -1: return text
    
    parts = para.split(split_marker)
    if len(parts) != 2:
        print(f"Error splitting {tag_base} with marker: {split_marker}")
        return text
    
    a = parts[0].strip()
    a = a.replace(f"[{tag_base}]", f"[{part_a}]")
    b = f"[{part_b}] " + split_marker + parts[1]
    
    text[start_idx] = a + "\n\n" + b
    return text

en_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_en.txt'
ko_file = r'c:\git_repo\TKprof_book\books\dracula\chapters\ch27_ko.txt'

with open(en_file, 'r', encoding='utf-8') as f:
    en_lines = f.readlines()
with open(ko_file, 'r', encoding='utf-8') as f:
    ko_lines = f.readlines()

# P003
en_lines = split_text(en_lines, "The Professor was tireless.", "P003", "P003a", "P003b")
ko_lines = split_text(ko_lines, "교수님은 지칠 줄을 모르셨다.", "P003", "P003a", "P003b")

# P017
en_lines = split_text(en_lines, "Then we lay down next to the campfire", "P017", "P017a", "P017b")
ko_lines = split_text(ko_lines, "그러고 나서 우리는 모피를 두른 채 모닥불 옆에 누웠고", "P017", "P017a", "P017b")

# P027_028
en_lines = split_text(en_lines, "Uncontrollable fear washed over me,", "P027_028", "P027_028a", "P027_028b")
ko_lines = split_text(ko_lines, "걷잡을 수 없는 두려움이 엄습했지만,", "P027_028", "P027_028a", "P027_028b")

# P073d
en_lines = split_text(en_lines, "When I informed the Professor of this in an overwhelmed voice,", "P073d", "P073da", "P073db")
ko_lines = split_text(ko_lines, "내가 벅찬 목소리로 교수님께 이 사실을 알리자,", "P073d", "P073da", "P073db")

# P079d
en_lines = split_text(en_lines, "Meanwhile, Mr. Morris was fighting a bloody battle", "P079d", "P079da", "P079db")
ko_lines = split_text(ko_lines, "그사이 모리스 씨는 지가니(집시)들이 겹겹이 둘러싼 방어 진형을 뚫어내느라", "P079d", "P079da", "P079db")

with open(en_file, 'w', encoding='utf-8') as f:
    f.writelines(en_lines)
with open(ko_file, 'w', encoding='utf-8') as f:
    f.writelines(ko_lines)
print("Done")
