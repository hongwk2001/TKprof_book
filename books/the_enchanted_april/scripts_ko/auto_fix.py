import json
import os

d = r'd:\git_repo\TKprof_book\books\the_enchanted_april\scripts_ko'
female_keywords = ['캐롤라인', '스크랩', '피셔', '코스탄자', '코스탄차', '프란체스카', '로티', '로즈', '그녀', '부인']
male_keywords = ['멜러쉬', '윌킨스', '프레더릭', '아버스넛', '브릭스', '도메니코', '목사', '그', '씨']

def is_female(ctx):
    f_idx = min([ctx.find(k) for k in female_keywords if k in ctx] + [999999])
    m_idx = min([ctx.find(k) for k in male_keywords if k in ctx] + [999999])
    return f_idx < m_idx

for ch in range(15, 23):
    path = os.path.join(d, f'script_ch_{ch}.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    modified = False
    for i, b in enumerate(data):
        if b.get('character') == 'Other':
            ctx = ''
            for j in range(max(0, i-2), min(len(data), i+3)):
                ctx += data[j]['text'] + ' '
                
            if is_female(ctx):
                # Check for some edge cases where it's definitely male
                if "윌킨스 씨가 말했다" in ctx and "그녀" in ctx:
                    # 'Mr. Wilkins said' takes precedence over 'she' if it's the exact speaker
                    speaker_is_male = False
                    if "윌킨스 씨가 말했다" in data[max(0, i-1)]['text'] or "윌킨스 씨가 말했다" in data[min(len(data)-1, i+1)]['text']:
                        speaker_is_male = True
                    if not speaker_is_male:
                        b['character'] = 'Rose'
                        b['voice'] = 'ko-KR-SunHiNeural'
                        b['speed'] = 0.95
                        modified = True
                else:
                    b['character'] = 'Rose'
                    b['voice'] = 'ko-KR-SunHiNeural'
                    b['speed'] = 0.95
                    modified = True
                    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Updated ch {ch}")
