import json
import os

d = r'd:\git_repo\TKprof_book\books\the_enchanted_april\scripts_ko'
with open('other_context.txt', 'w', encoding='utf-8') as out:
    for ch in range(15, 23):
        path = os.path.join(d, f'script_ch_{ch}.json')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for i, b in enumerate(data):
            if b.get('character') == 'Other':
                ctx_b = data[i-1]['text'] if i>0 else ''
                ctx_a = data[i+1]['text'] if i<len(data)-1 else ''
                
                female = any(x in ctx_b or x in ctx_a for x in ['캐롤라인', '스크랩', '피셔', '코스탄자', '프란체스카', '부인'])
                male = any(x in ctx_b or x in ctx_a for x in ['멜러쉬', '윌킨스', '프레더릭', '아버스넛', '브릭스', '도메니코', '목사'])
                
                if female and not male:
                    out.write(f'CH{ch} BLOCK {i} (FEMALE): {b["text"]}\n  PREV: {ctx_b}\n  NEXT: {ctx_a}\n')
                elif male and not female:
                    pass # out.write(f'CH{ch} BLOCK {i} (MALE): ...\n')
                else:
                    out.write(f'CH{ch} BLOCK {i} (AMBIGUOUS): {b["text"]}\n  PREV: {ctx_b}\n  NEXT: {ctx_a}\n')
