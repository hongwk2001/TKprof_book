import os
import re

base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"
postpositions = ['은', '는', '이', '가', '을', '를', '과', '와', '으로', '로', '에', '의', '도', '만', '까지', '부터', '에서']

def has_jongseong(char):
    if not ('가' <= char <= '힣'):
        return False
    return (ord(char) - 0xAC00) % 28 > 0

def get_correct_postposition(char, pos):
    if not ('가' <= char <= '힣'):
        return pos
        
    has_j = has_jongseong(char)
    
    if pos in ['은', '는']:
        return '은' if has_j else '는'
    if pos in ['이', '가']:
        return '이' if has_j else '가'
    if pos in ['을', '를']:
        return '을' if has_j else '를'
    if pos in ['과', '와']:
        return '과' if has_j else '와'
    if pos in ['으로', '로']:
        # 'ㄹ' batchim acts like no batchim for '로'
        if has_j and (ord(char) - 0xAC00) % 28 != 8:
            return '으로'
        else:
            return '로'
            
    return pos

def fix_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern for word + comma + postposition
    pattern = r'([가-힣]),(' + '|'.join(postpositions) + r')\b'
    
    def replace_comma(match):
        last_char = match.group(1)
        original_pos = match.group(2)
        correct_pos = get_correct_postposition(last_char, original_pos)
        return last_char + correct_pos

    new_content, count = re.subn(pattern, replace_comma, content)
    
    # Also fix dangling commas before spaces and Korean modifiers (e.g., "받아들이는, 책임을 졌고" -> "받아들이는 책임을 졌고")
    # This is a bit riskier, let's just stick to the obvious postposition errors as planned.
    
    if count > 0:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Fixed {count} comma issues in {os.path.basename(filepath)}")

for b in range(1, 5):
    b_dir = os.path.join(base_dir, f"book{b}")
    if not os.path.exists(b_dir): continue
    
    for c in range(1, 10):
        key = f"book{b}_ch{c:02d}"
        ko_file = os.path.join(b_dir, f"{key}_ko.txt")
        if os.path.exists(ko_file):
            fix_file(ko_file)
