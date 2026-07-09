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
        lines = f.readlines()
    
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    chunks = []
    
    for i, b in enumerate(data):
        if b.get('character') == 'Other':
            # Gather context
            ctx = ''
            for j in range(max(0, i-2), min(len(data), i+3)):
                ctx += data[j]['text'] + ' '
                
            if is_female(ctx):
                # We need to find the line number of this block in the file
                # The file is pretty-printed JSON. We can find the exact text
                # We will look for `"text": "..."` and the preceding `"character": "Other"`
                
                text_snippet = json.dumps(b['text'], ensure_ascii=False)
                
                # We'll just replace the `"character": "Other"` in that specific block.
                # To do this safely, we can find the line index where this text appears,
                # then go backwards to find the "character" line.
                pass

    # Actually, a much easier way: Just modify the JSON directly in python,
    # but the user requested `multi_replace_file_content`.
    # I can just generate `multi_replace_file_content` arguments!
    
    # Wait, the instruction says: "Use `multi_replace_file_content` or `replace_file_content` to fix the JSON files."
    # If I just generate the exact string replacement chunks:
    # TargetContent:
    # "character": "Other",
    # "voice": "ko-KR-HyunsuMultilingualNeural",
    # "speed": 1.05
    # ReplacementContent:
    # "character": "Rose",
    # "voice": "ko-KR-SunHiNeural",
    # "speed": 0.95
    # Since I don't know the exact spacing, I can search for "Other" in lines and get the line number.
