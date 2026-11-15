import re
import os

def clean_tag(text):
    return re.sub(r'^\[P[0-9a-zA-Z_]+\]\s*', '', text.strip())

def process_file(filepath, is_korean):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')
        
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    
    new_paras = []
    
    for p in paras:
        # 1. Handle P036 & P037_038
        if p.startswith('[P036]'):
            clean_text = clean_tag(p)
            if not is_korean:
                # Split English
                split_point = 'His voice was growing fainter, and his breathing was getting worse. Van Helsing stood up instinctively.'
                parts = clean_text.split(split_point)
                p1 = parts[0].strip() + ' ' + split_point
                p2 = parts[1].strip()
                new_paras.append(f"[P036] {p1}")
                new_paras.append(f"[P037] {p2}")
            else:
                # Split Korean
                split_point = '그의 목소리는 점점 더 희미해졌고 숨소리는 더욱 거칠어졌습니다. 반 헬싱 박사님이 본능적으로 벌떡 일어섰습니다.'
                parts = clean_text.split(split_point)
                p1 = parts[0].strip() + ' ' + split_point
                p2 = parts[1].strip()
                new_paras.append(f"[P036] {p1}")
                new_paras.append(f"[P037] {p2}")
                
        elif p.startswith('[P037_038]'):
            clean_text = clean_tag(p)
            new_paras.append(f"[P038] {clean_text}")
            
        # 2. Handle P045 -> P045a, P045b, P045c
        elif p.startswith('[P045]'):
            clean_text = clean_tag(p)
            if not is_korean:
                # Split 1: scar on his forehead.
                # Split 2: he turned and lunged at us.
                part1 = clean_text.split('scar on his forehead.')[0].strip() + ' scar on his forehead.'
                rest = clean_text.split('scar on his forehead.')[1].strip()
                part2 = rest.split('he turned and lunged at us.')[0].strip() + ' he turned and lunged at us.'
                part3 = rest.split('he turned and lunged at us.')[1].strip()
            else:
                # Split 1: 이마의 흉터까지도 백작이라는 것을 단번에 알아차렸습니다.
                # Split 2: 우리에게 덤벼들었습니다.
                part1 = clean_text.split('이마의 흉터까지도 백작이라는 것을 단번에 알아차렸습니다.')[0].strip() + ' 이마의 흉터까지도 백작이라는 것을 단번에 알아차렸습니다.'
                rest = clean_text.split('이마의 흉터까지도 백작이라는 것을 단번에 알아차렸습니다.')[1].strip()
                part2 = rest.split('우리에게 덤벼들었습니다.')[0].strip() + ' 우리에게 덤벼들었습니다.'
                part3 = rest.split('우리에게 덤벼들었습니다.')[1].strip()
                
            new_paras.append(f"[P045a] {part1}")
            new_paras.append(f"[P045b] {part2}")
            new_paras.append(f"[P045c] {part3}")
            
        # 3. Handle P062_063 -> P062, P063
        elif p.startswith('[P062_063]'):
            clean_text = clean_tag(p)
            if not is_korean:
                part1 = clean_text.split('organize her thoughts, she began:')[0].strip() + ' organize her thoughts, she began:'
                part2 = clean_text.split('organize her thoughts, she began:')[1].strip()
            else:
                part1 = clean_text.split('마침내 입을 열었습니다.')[0].strip() + ' 마침내 입을 열었습니다.'
                part2 = clean_text.split('마침내 입을 열었습니다.')[1].strip()
                
            new_paras.append(f"[P062] {part1}")
            new_paras.append(f"[P063] {part2}")
            
        # 4. Handle P066 -> P066a, P066b
        elif p.startswith('[P066]'):
            clean_text = clean_tag(p)
            if not is_korean:
                part1 = clean_text.split("And this is how we ensure that!'")[0].strip() + " And this is how we ensure that!'"
                part2 = clean_text.split("And this is how we ensure that!'")[1].strip()
            else:
                part1 = clean_text.split("그것을 위해 이렇게 하는 것이다!'")[0].strip() + " 그것을 위해 이렇게 하는 것이다!'"
                part2 = clean_text.split("그것을 위해 이렇게 하는 것이다!'")[1].strip()
                
            new_paras.append(f"[P066a] {part1}")
            new_paras.append(f"[P066b] {part2}")
            
        else:
            new_paras.append(p)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras))
        
    print(f"Successfully processed {filepath}: new paragraph count = {len(new_paras)}")

def main():
    process_file('books/dracula/chapters/ch21_en.txt', is_korean=False)
    process_file('books/dracula/chapters/ch21_ko.txt', is_korean=True)

if __name__ == '__main__':
    main()
