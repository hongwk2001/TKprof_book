import re

def fix_ch08_p033():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    paras = text.split('\n\n')
    new_paras = []
    
    i = 0
    while i < len(paras):
        p = paras[i].strip()
        m = re.match(r'^\[(P[a-zA-Z0-9_]+)\]', p)
        if m:
            pid = m.group(1)
            # Remove [P033] "경구,
            if pid == 'P033' and '경구' in p:
                i += 1
                continue
            
            # Decrement tags from P034 to P043
            if len(pid) >= 4 and pid[1:4].isdigit():
                num = int(pid[1:4])
                if 34 <= num <= 43:
                    new_num = num - 1
                    new_pid = f"P{new_num:03d}{pid[4:]}"
                    p = re.sub(r'^\[P[a-zA-Z0-9_]+\]', f'[{new_pid}]', p)
        
        new_paras.append(p)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')
        
    print("Fixed ch08_ko.txt successfully")

if __name__ == '__main__':
    fix_ch08_p033()
