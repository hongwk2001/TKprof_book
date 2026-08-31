import time
import re
from deep_translator import GoogleTranslator

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch23_en.txt', 'r', encoding='utf-8') as f:
    paras = [p for p in f.read().split('\n\n') if p.strip()]

def post_process(text):
    name_map = {
        'Count Dracula': '드라큘라 백작',
        'Jonathan Harker': '조나단 하커',
        'Mina Harker': '미나 하커',
        'Mina Murray': '미나 머레이',
        'Madam Mina': '미나 부인',
        'Mrs. Harker': '하커 부인',
        'Professor Abraham Van Helsing': '아브라함 반 헬싱 교수',
        'Van Helsing': '반 헬싱',
        'Lucy Westenra': '루시 웨스텐라',
        'Dr. John Seward': '존 수어드 박사',
        'Dr. Seward': '수어드 박사',
        'Arthur Holmwood': '아서 홈우드',
        'Lord Godalming': '고달밍 경',
        'Quincey Morris': '퀸시 모리스',
        'Quincey': '퀸시',
        'Renfield': '렌필드'
    }
    for eng, kor in name_map.items():
        text = text.replace(eng, kor)
        
    text = re.sub(r'\([a-zA-Z\s]+\)', '', text)
    text = text.replace("'", '"')
    text = text.replace('‘', '"').replace('’', '"').replace('“', '"').replace('”', '"')
    text = text.replace('*', '')
    
    if text.endswith('다.') and not text.endswith('습니다.') and not text.endswith('합니다.') and not text.endswith('입니다.'):
        text = text[:-2] + '습니다.'
        
    return text

ko_paras = []
translator = GoogleTranslator(source='en', target='ko')

for i, p in enumerate(paras):
    print(f'Translating {i}/{len(paras)}')
    try:
        translated = translator.translate(p)
        translated = post_process(translated)
        ko_paras.append(translated)
    except Exception as e:
        print(f'Error at {i}: {e}')
        ko_paras.append(p)
    time.sleep(0.5)

with open(r'c:\git_repo\TKprof_book\books\dracula\chapters\ch23_ko.txt', 'w', encoding='utf-8') as f:
    for p in ko_paras:
        f.write(p + '\n\n')
