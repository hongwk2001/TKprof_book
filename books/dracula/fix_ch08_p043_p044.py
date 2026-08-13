import re

def fix_ch08_p043_p044():
    filepath = 'chapters/ch08_ko.txt'
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    paras = [p.strip() for p in text.split('\n\n') if p.strip()]

    # We need to find P043a, P043b, P043c (or P044a, P044b, P044c containing these texts) and merge them into P043.
    # P043a text: "그때 내 불쌍한 작은 발은..."
    # P043b text: "그녀는 대답하기 전 미간을..."
    # P043c text: "그가 왜 반했는지..."

    # Lucy's dream parts:
    # "꿈이라기엔 모든 게 너무 생생했어..." -> P044a
    # "그러다 마치 지진이라도..." -> P044b (or part of P044a/b/c)
    # "그러고는 모든 게 멀어지는..." -> P044c

    new_paras = []
    i = 0
    while i < len(paras):
        p = paras[i]
        
        # Check if this is the start of the split P043 block
        if ('그때 내 불쌍한' in p) or ('P043a' in p[:10]) or ('P044a' in p[:10] and '그때 내 불쌍한' in p):
            # Collect the next 2 paragraphs if they are the continuation of P043
            p1 = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            i += 1
            p2 = ""
            p3 = ""
            
            if i < len(paras) and ('그녀는 대답하기' in paras[i]):
                p2 = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', paras[i])
                i += 1
            if i < len(paras) and ('그가 왜 반했는지' in paras[i]):
                p3 = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', paras[i])
                i += 1
                
            merged_p043 = f"[P043] {p1} {p2} {p3}".strip()
            # Clean any double spaces
            merged_p043 = re.sub(r'\s+', ' ', merged_p043)
            new_paras.append(merged_p043)
            continue

        # Now fix Lucy's dream tags to match EN P044a, P044b, P044c
        if '꿈이라기엔 모든 게' in p:
            clean_text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            new_paras.append(f"[P044a] {clean_text}")
        elif '그러다 마치 지진' in p:
            clean_text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            new_paras.append(f"[P044b] {clean_text}")
        elif '그러고는 모든 게 멀어지는' in p:
            clean_text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            new_paras.append(f"[P044c] {clean_text}")
        elif '그러고서 루시는 웃음을' in p:
            clean_text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            new_paras.append(f"[P045a] {clean_text}")
        elif '어머니도 그런 루시의' in p:
            clean_text = re.sub(r'^\[P[a-zA-Z0-9_]+\]\s*', '', p)
            new_paras.append(f"[P045b] {clean_text}")
        else:
            new_paras.append(p)
        i += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras) + '\n')

    print("Successfully merged P043 and re-tagged P044a-c, P045a-b!")

if __name__ == '__main__':
    fix_ch08_p043_p044()
