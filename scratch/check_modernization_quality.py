import glob
import os
import difflib

base_dir = r"d:\git_repo\TKprof_book\books\seneca_emotional_resilience\chapters"

issues = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith("_en.txt"):
            mod_path = os.path.join(root, f)
            # Find the corresponding raw file
            # e.g., on_anger_book2_ch07_en.txt -> raw_on_anger_book2_ch07.txt
            raw_name = "raw_" + f.replace("_en.txt", ".txt")
            raw_path = os.path.join(root, raw_name)
            
            if os.path.exists(raw_path):
                with open(raw_path, 'r', encoding='utf-8') as file_r:
                    raw_text = file_r.read().strip()
                with open(mod_path, 'r', encoding='utf-8') as file_m:
                    mod_text = file_m.read().strip()
                
                # Strip the chapter headers for comparison
                # raw has e.g. VII. at the start, mod has [Chapter 7]
                r_lines = [l.strip() for l in raw_text.split('\n') if l.strip()]
                m_lines = [l.strip() for l in mod_text.split('\n') if l.strip()]
                
                if r_lines and r_lines[0].split('.')[0].strip().replace('I','').replace('V','').replace('X','').replace('L','') == '':
                    r_text_compare = " ".join(r_lines[1:])
                else:
                    r_text_compare = " ".join(r_lines)
                    
                if m_lines and m_lines[0].startswith('[') and m_lines[0].endswith(']'):
                    m_text_compare = " ".join(m_lines[1:])
                else:
                    m_text_compare = " ".join(m_lines)
                
                # Calculate ratio
                ratio = difflib.SequenceMatcher(None, r_text_compare, m_text_compare).ratio()
                if ratio > 0.90:
                    issues.append((mod_path, ratio))

print(f"Total potential quality gaps found: {len(issues)}")
for path, ratio in sorted(issues):
    print(f"  {os.path.basename(path)} is {ratio:.1%} similar to its raw text")
