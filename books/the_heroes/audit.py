import json
from pathlib import Path

files_to_check = [
    r'c:\git_repo\TKprof_book\books\the_heroes\json\ch_00.json',
    r'c:\git_repo\TKprof_book\books\the_heroes\json\ch_01.json'
]

required_fields = {'id', 'tag', 'chapter_id', 'story', 'part', 'raw', 'en', 'ko', 'is_header', 'word_count'}

def check_file(filepath):
    print(f'\n--- Auditing {filepath} ---')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'Error reading {filepath}: {e}')
        return
    
    total_items = len(data)
    total_sentences = 0
    lengths = []
    
    schema_ok = True
    en_schema_ok = True
    len_ok = True
    id_continuity_ok = True
    sentence_id_ok = True
    
    last_id = 0
    
    for i, item in enumerate(data):
        # 1. Schema Consistency
        missing_fields = required_fields - set(item.keys())
        if missing_fields:
            schema_ok = False
            print(f'Item index {i} missing fields: {missing_fields}')
            
        # Check en format
        en = item.get('en', [])
        if not isinstance(en, list):
            en_schema_ok = False
        else:
            for sen in en:
                if not isinstance(sen, dict) or 'id' not in sen or 'text' not in sen:
                    en_schema_ok = False
                elif not isinstance(sen['id'], int) or not isinstance(sen['text'], str):
                    en_schema_ok = False
                    
        # 3. Paragraph & ID Continuity
        curr_id = item.get('id')
        if curr_id != last_id + 1:
            id_continuity_ok = False
            print(f'Paragraph ID break: expected {last_id + 1}, got {curr_id}')
        last_id = curr_id
        
        # Sentence IDs
        if isinstance(en, list):
            last_sen_id = 0
            for sen in en:
                s_id = sen.get('id')
                s_text = sen.get('text', '')
                
                if s_id != last_sen_id + 1:
                    sentence_id_ok = False
                    print(f'Sentence ID break in item {curr_id}: expected {last_sen_id + 1}, got {s_id}')
                last_sen_id = s_id
                
                # Length check
                t_len = len(s_text)
                lengths.append(t_len)
                if t_len > 200:
                    len_ok = False
                    print(f'Sentence too long ({t_len} chars) in item {curr_id}, sen {s_id}')
                total_sentences += 1
                
    print(f'Schema Consistency: {schema_ok}')
    print(f'en Schema Strict: {en_schema_ok}')
    print(f'Max length <= 200: {len_ok}')
    print(f'Paragraph ID continuity: {id_continuity_ok}')
    print(f'Sentence ID continuity: {sentence_id_ok}')
    print(f'Total items: {total_items}')
    
    if lengths:
        print(f'Metrics: Total items={total_items}, Total sentences={total_sentences}, Min={min(lengths)}, Max={max(lengths)}, Avg={sum(lengths)/len(lengths):.2f}')
    else:
        print('No sentences found.')

for f in files_to_check:
    check_file(f)

