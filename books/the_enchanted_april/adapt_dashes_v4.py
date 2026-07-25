import os

base_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
tagged_dir = os.path.join(base_dir, "tagged")

def fix_last(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    content = content.replace("그의 젊은 시절—그가 여전히", "그의 젊은 시절, 그가 여전히")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed final dash in {os.path.basename(filepath)}")

fix_last(os.path.join(base_dir, "ch_21_ko.txt"))
fix_last(os.path.join(tagged_dir, "tagged_ch_21_ko.txt"))
