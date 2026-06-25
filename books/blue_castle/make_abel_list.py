import os
import re

d = 'D:/git_repo/TKprof_book/books/blue_castle/chapters'
out_file = r'C:\Users\hongw\.gemini\antigravity\brain\6d783c09-187c-4c51-ada1-e656e52cc105\abel_replacements.md'

with open(out_file, 'w', encoding='utf-8') as out:
    out.write('# 📋 "Roaring Abel" Replacement List\n\n')
    out.write('Here is every line where "에이블" (Abel) appears in the Korean translation. \n')
    out.write('Currently, he is referred to as **로어링 에이블** (Roaring Abel) or simply **에이블** (Abel).\n\n')
    out.write('> [!IMPORTANT]\n> Please review how you would like these changed. I can replace:\n')
    out.write('> - `로어링 에이블` -> `고함쟁이 에이블`\n')
    out.write('> - And leave `에이블` alone when used by itself.\n> OR replace all instances with `고함쟁이 에이블`.\n\n')

    total = 0
    for i in range(1, 46):
        f = f'ch_{i:02d}_ko.txt'
        path = os.path.join(d, f)
        if not os.path.exists(path): continue
        
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        found_in_file = False
        for line_num, line in enumerate(lines):
            line = line.strip()
            if '에이블' in line:
                if not found_in_file:
                    out.write(f'## Chapter {i}\n')
                    found_in_file = True
                
                highlighted = line.replace('에이블', '**에이블**')
                out.write(f'- **Line {line_num+1}:** {highlighted}\n')
                total += 1
                
        if found_in_file:
            out.write('\n')
            
    out.write(f'\n**Total occurrences found:** {total}\n')
