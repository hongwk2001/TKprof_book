import os
import re

base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"

def fix_quotes():
    for b in range(1, 5):
        b_dir = os.path.join(base_dir, f"book{b}")
        if not os.path.exists(b_dir): continue
        
        for c in range(1, 10):
            key = f"book{b}_ch{c:02d}"
            ko_file = os.path.join(b_dir, f"{key}_ko.txt")
            if os.path.exists(ko_file):
                with open(ko_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Replace ," with ", and ,' with ',
                new_content = re.sub(r',"', '",', content)
                new_content = re.sub(r',\'', '\',', new_content)
                # Also handle full-width comma if any
                new_content = re.sub(r'，"', '"，', new_content)
                new_content = re.sub(r'，\'', '\'，', new_content)
                
                if new_content != content:
                    with open(ko_file, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Fixed quotes in {key}")

if __name__ == "__main__":
    fix_quotes()
