import sys
import os
sys.path.append('books/dracula')
from map_and_tag_paragraphs import map_and_tag_chapter

def clean_tag(text):
    import re
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def main():
    filepath = 'books/dracula/chapters/ch25_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    new_paras = []
    
    for p in paras:
        if p.startswith('[P061]'):
            clean_text = clean_tag(p)
            split_point = '우리는 저마다 다른 방식으로 그 충격을 받아들였다.'
            parts = clean_text.split(split_point)
            p1 = parts[0].strip() + ' ' + split_point
            p2 = parts[1].strip()
            new_paras.append(p1)
            new_paras.append(p2)
            
        elif p.startswith('[P078]'):
            clean_text = clean_tag(p)
            split_point = '진정한 범죄자는 항상 한 가지 유형의 범죄만을 저지르오.'
            parts = clean_text.split(split_point)
            p1 = parts[0].strip()
            p2 = split_point + ' ' + parts[1].strip()
            new_paras.append(p1)
            new_paras.append(p2)
            
        else:
            new_paras.append(p)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras))
        
    print("Processed ch25_ko.txt splits.")
    
    # Now run map_and_tag_chapter(25) to automatically map and tag them correctly!
    map_and_tag_chapter(25)

if __name__ == '__main__':
    main()
