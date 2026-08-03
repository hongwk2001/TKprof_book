import os
import re

base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"

def audit_quotes():
    output = []
    for b in range(1, 5):
        b_dir = os.path.join(base_dir, f"book{b}")
        if not os.path.exists(b_dir): continue
        
        for c in range(1, 10):
            key = f"book{b}_ch{c:02d}"
            ko_file = os.path.join(b_dir, f"{key}_ko.txt")
            if os.path.exists(ko_file):
                with open(ko_file, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Find ," or ,'
                pattern = r'([가-힣]+)(,|，)(["\'])(\s+)([가-힣]+)'
                matches = re.finditer(pattern, content)
                for m in matches:
                    start = max(0, m.start() - 30)
                    end = min(len(content), m.end() + 30)
                    output.append(f"{key}: ...{content[start:end]}...")
                    
    with open(r"c:\git_repo\TKprof_book\scratch\quote_audit.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    audit_quotes()
