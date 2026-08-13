import os
import re

def fix_ch08():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    paras = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    new_paras = []
    i = 0
    while i < len(paras):
        p = paras[i]
        m = re.match(r'^\[(P[0-9a-zA-Z_]+)\]', p)
        if not m:
            new_paras.append(p)
            i += 1
            continue
            
        pid = m.group(1)
        
        # If we hit P032, we merge it with P033
        if pid == 'P032':
            # p is P032
            # paras[i+1] should be P033
            next_p = paras[i+1]
            next_m = re.match(r'^\[P033\]\s*(.*)', next_p, flags=re.DOTALL)
            if next_m:
                merged = p + ' ' + next_m.group(1)
                new_paras.append(merged)
                i += 2  # skip P033
                continue
        elif pid.startswith('P') and len(pid) >= 4 and pid[1:4].isdigit():
            # Decrement any Pxxx > 033
            num_part = int(pid[1:4])
            if num_part >= 34:
                new_num = num_part - 1
                # Format back to Pxxx, preserving any suffix like 'a', 'b', 'c'
                new_pid = f"P{new_num:03d}{pid[4:]}"
                p = re.sub(r'^\[P[0-9a-zA-Z_]+\]', f'[{new_pid}]', p)
        
        new_paras.append(p)
        i += 1
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')
        
    print(f"Fixed {filepath}")

if __name__ == '__main__':
    fix_ch08()
