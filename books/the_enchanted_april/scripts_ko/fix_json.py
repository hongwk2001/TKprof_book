import json
import os

d = r'd:\git_repo\TKprof_book\books\the_enchanted_april\scripts_ko'
with open(r'd:\git_repo\TKprof_book\books\the_enchanted_april\scripts_ko\fix_json.py', 'w', encoding='utf-8') as script_file:
    script_file.write("""import json
import os

d = r'd:\\git_repo\\TKprof_book\\books\\the_enchanted_april\\scripts_ko'
female_keywords = ['캐롤라인', '스크랩', '피셔', '코스탄자', '프란체스카', '그녀', '부인', '로티', '로즈', '할머니']
male_keywords = ['멜러쉬', '윌킨스', '프레더릭', '아버스넛', '브릭스', '도메니코', '목사', '그']

for ch in range(15, 23):
    path = os.path.join(d, f'script_ch_{ch}.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for i, b in enumerate(data):
        if b.get('character') == 'Other':
            ctx_b = data[i-1]['text'] if i>0 else ''
            ctx_a = data[i+1]['text'] if i<len(data)-1 else ''
            
            # Simple heuristic, but to be sure we can just replace all for now and see?
            # Wait, the instructions said: "If the speaker is a FEMALE character (Lady Caroline/Scrap, Mrs. Fisher, Costanza, Francesca, etc.), change their mapping to: character: Rose, voice: ko-KR-SunHiNeural, speed: 0.95"
            # Since I have to use `replace_file_content` or `multi_replace_file_content`, I should probably let python generate a patch file or just update the file directly.
            pass
""")
