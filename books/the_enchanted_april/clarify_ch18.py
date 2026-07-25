import os

replacements = {
    # Line 8
    "그가 지적인 사람이기를 바랐다. 그래야 그의 찬사가 더욱 가치 있어질 테니까.":
    "브릭스가 지적인 사람이기를 바랐다. 그래야 그의 찬사가 더욱 가치 있어질 테니까.",
    
    # Line 12
    "그는 고아이자 외동아들이었고, 본래 가정적인 성품을 지닌 남자였다.":
    "브릭스는 고아이자 외동아들이었고, 본래 가정적인 성품을 지닌 남자였다.",
    
    # Line 14
    "그는 등대를 향해 걸어가는 동안 사랑스러운 이름의 이 여인과":
    "브릭스는 등대를 향해 걸어가는 동안 사랑스러운 이름의 이 여인과",
    
    "이토록 빠르게 마음을 열어버린다는 생각에 그는 저도 모르게 웃음이 나왔다.":
    "이토록 빠르게 마음을 열어버린다는 생각에 브릭스는 저도 모르게 웃음이 나왔다.",
    
    # Line 21
    "그가 다시 웃음을 터뜨렸다. “괜찮습니다, 익숙하니까요. 제겐 아무도 없어요. 형제나 자매도 없고요.”":
    "브릭스가 다시 웃음을 터뜨렸다. “괜찮습니다, 익숙하니까요. 제겐 아무도 없어요. 형제나 자매도 없고요.”",
    
    # Line 31
    "그는 이처럼 다정한 말들을 연달아 건넸다.":
    "브릭스는 이처럼 다정한 말들을 연달아 건넸다.",
    
    # Line 73
    "그는 말을 멈추고 얼굴을 붉혔다. “제가 여기 살지 않는다는 사실을 깜빡 잊었군요.”":
    "브릭스는 말을 멈추고 얼굴을 붉혔다. “제가 여기 살지 않는다는 사실을 깜빡 잊었군요.”"
}

base_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
tagged_dir = os.path.join(base_dir, "tagged")

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        if old in content:
            content = content.replace(old, new)
            
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {os.path.basename(filepath)}")

fix_file(os.path.join(base_dir, "ch_18_ko.txt"))
fix_file(os.path.join(tagged_dir, "tagged_ch_18_ko.txt"))

print("Pronoun clarification in Ch 18 complete.")
