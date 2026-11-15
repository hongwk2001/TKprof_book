import sys
import os
sys.path.append('books/dracula')
from map_and_tag_paragraphs import map_and_tag_chapter

def clean_tag(text):
    import re
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def process_file(filepath, is_korean):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    new_paras = []
    
    for p in paras:
        if p.startswith('[P086]'):
            clean_text = clean_tag(p)
            if not is_korean:
                split_point = 'After Arthur and Quincey left for the station'
            else:
                split_point = '아서와 퀸시가 역으로 떠난 뒤'
                
            parts = clean_text.split(split_point)
            p1 = parts[0].strip()
            p2 = split_point + parts[1]
            new_paras.append(p1) # Tag will be assigned by map_and_tag_chapter
            new_paras.append(p2)
            
        elif p.startswith('[P087]'):
            clean_text = clean_tag(p)
            if not is_korean:
                split_point = 'When I think of the poor boy Arthur'
            else:
                split_point = '가엾은 아서 소년을 생각하면'
                
            parts = clean_text.split(split_point)
            p1 = parts[0].strip()
            p2 = split_point + parts[1]
            new_paras.append(p1)
            new_paras.append(p2)
            
        elif p.startswith('[P103]'):
            clean_text = clean_tag(p)
            if not is_korean:
                split_point = 'Because the first child to go missing stated'
            else:
                split_point = '첫 번째로 실종되었던 아이가'
                
            parts = clean_text.split(split_point)
            p1 = parts[0].strip()
            p2 = split_point + parts[1]
            new_paras.append(p1)
            new_paras.append(p2)
            
        else:
            new_paras.append(p)
            
    # Write back without tags (since map_and_tag_chapter will tag them)
    # Actually, we can keep the tags for other paragraphs, map_and_tag_chapter will strip them anyway
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras))
        
    print(f"Processed {filepath}")

def main():
    # 1. Perform splits
    process_file('books/dracula/chapters/ch13_en.txt', is_korean=False)
    process_file('books/dracula/chapters/ch13_ko.txt', is_korean=True)
    
    # 2. Re-run map_and_tag_chapter to tag them correctly
    map_and_tag_chapter(13)

if __name__ == '__main__':
    main()
