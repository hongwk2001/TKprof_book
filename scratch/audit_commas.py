import os
import re

base_dir = r"c:\git_repo\TKprof_book\books\tono_bungay\chapters"
postpositions = ['에', '는', '은', '를', '을', '가', '이', '의', '로', '으로', '과', '와', '도', '만', '까지', '부터', '에서']

def audit_commas():
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
                
                # Find all occurrences of word + comma + postposition
                pattern = r'([\w가-힣]+),(' + '|'.join(postpositions) + r')\b'
                matches = re.finditer(pattern, content)
                for m in matches:
                    start = max(0, m.start() - 20)
                    end = min(len(content), m.end() + 20)
                    output.append(f"{key}: ...{content[start:end]}...")
                    
                # Find commas before spaces inside quotes or similar weird things like "받아들이는,"
                pattern2 = r'([가-힣]+),\s*(["\'])'
                matches2 = re.finditer(pattern2, content)
                for m in matches2:
                    start = max(0, m.start() - 20)
                    end = min(len(content), m.end() + 20)
                    output.append(f"{key} (quote): ...{content[start:end]}...")
                    
                # Find dangling commas like "받아들이는, 책임을 졌고" where it should just be "받아들이는 책임을 졌고" (verb modifier)
                pattern3 = r'([가-힣]+(는|은|를|을|가|이)),\s+([가-힣]+)'
                matches3 = re.finditer(pattern3, content)
                for m in matches3:
                    start = max(0, m.start() - 20)
                    end = min(len(content), m.end() + 20)
                    output.append(f"{key} (modifier): ...{content[start:end]}...")
                    
    with open(r"c:\git_repo\TKprof_book\scratch\comma_audit.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output))

if __name__ == "__main__":
    audit_commas()
