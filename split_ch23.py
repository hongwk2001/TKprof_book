import sys

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old_str, new_str in replacements:
        if old_str not in content:
            print(f"Error: Could not find '{old_str}' in {filepath}")
            sys.exit(1)
        content = content.replace(old_str, new_str)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully updated {filepath}")

en_replacements = [
    ("[P009]", "[P009a]"),
    ("hideouts! But, my boy", "hideouts!\n\n[P009b] But, my boy"),
    ("[P024]", "[P024a]"),
    ("floor. The expression", "floor.\n\n[P024b] The expression")
]

ko_replacements = [
    ("[P009]", "[P009a]"),
    ("은신처라는 걸 몰랐을 테니까! 하지만, 내 아이야", "은신처라는 걸 몰랐을 테니까!\n\n[P009b] 하지만, 내 아이야"),
    ("[P024]", "[P024a]"),
    ("금화가 바닥으로 쏟아졌다. 백작의 얼굴에", "금화가 바닥으로 쏟아졌다.\n\n[P024b] 백작의 얼굴에")
]

replace_in_file(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch23_en.txt', en_replacements)
replace_in_file(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch23_ko.txt', ko_replacements)
