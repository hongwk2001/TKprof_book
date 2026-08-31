import re

def fix_ch08_remove_extra_p047():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    new_paras = []
    i = 0
    while i < len(paras):
        p = paras[i]
        
        # Check for the extra separator P047
        if re.match(r'^\[P047\]\s*\*+\s*\*+\s*\*+\s*\*+\s*\*+', p):
            print("Removing extra P047 separator line")
            i += 1
            continue

        m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
        if m:
            pid = m.group(1)
            # Re-map tags starting from P048a -> P047, P048b -> P048a, etc.
            # We decrement any numeric tag >= 48 by 1 (or re-map specific suffixes)
            if pid == 'P048a' and '8월 19일' in p:
                p = re.sub(r'^\[P048a\]', '[P047]', p)
            elif pid == 'P048b' and '부다페스트' in p:
                p = re.sub(r'^\[P048b\]', '[P048a]', p)
            elif pid == 'P049' and '윌헬미나' in p:
                p = re.sub(r'^\[P049\]', '[P048b]', p)
            elif pid == 'P050' and '8월 12일' in p:
                p = re.sub(r'^\[P050\]', '[P049]', p)
            elif pid == 'P051a' and '친애하는' in p:
                p = re.sub(r'^\[P051a\]', '[P050]', p)
            elif pid == 'P051b' and '직접 펜을' in p:
                p = re.sub(r'^\[P051b\]', '[P051a]', p)
            elif pid == 'P053' and '피터 호킨스' in p:
                p = re.sub(r'^\[P053\]', '[P051b]', p)
            elif pid == 'P053b' and '안녕히 계십시오' in p:
                p = re.sub(r'^\[P053b\]', '[P053]', p)
            elif pid == 'P054' and '깊은 연민' in p:
                p = re.sub(r'^\[P054\]', '[P053b]', p)
            elif pid == 'P055a' and '아가타 수녀' in p:
                p = re.sub(r'^\[P055a\]', '[P054]', p)
            elif pid == 'P055b' and '추신' in p:
                p = re.sub(r'^\[P055b\]', '[P055a]', p)
            elif pid == 'P055c' and '당분간은' in p:
                p = re.sub(r'^\[P055c\]', '[P055b]', p)
            elif pid == 'P056' and '그 난폭한' in p:
                p = re.sub(r'^\[P056\]', '[P055c]', p)
            elif len(pid) >= 4 and pid[1:4].isdigit():
                num = int(pid[1:4])
                if num >= 57:
                    new_num = num - 1
                    new_pid = f"P{new_num:03d}{pid[4:]}"
                    p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{new_pid}]', p)

        new_paras.append(p)
        i += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')

    print("Removed extra P047 separator and re-aligned all subsequent tags!")

if __name__ == '__main__':
    fix_ch08_remove_extra_p047()
