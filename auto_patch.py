import json
import re

my_transcript = 'C:/Users/hongw/.gemini/antigravity/brain/e163a63a-2cbe-4581-a0f5-bb5111640f9d/.system_generated/logs/transcript.jsonl'
target_file = 'c:/git_repo/TKprof_book/books/two_cities/json/book1_ch_05.json'

with open(target_file, 'r', encoding='utf-8') as f:
    target_data = json.load(f)

patch_dict = {}

with open(my_transcript, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            entry = json.loads(line)
            content = entry.get('content', '')
            if 'MESSAGE_PRIORITY_HIGH' in content or 'tag' in content:
                # find JSON array string in content
                match = re.search(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
                if match:
                    json_str = match.group(0)
                    try:
                        parsed = json.loads(json_str)
                        for item in parsed:
                            if 'tag' in item and ('ko' in item or 'en' in item):
                                patch_dict[item['tag']] = item
                    except:
                        pass
        except:
            pass

patched_count = 0
for item in target_data:
    if item['tag'] in patch_dict:
        patch_item = patch_dict[item['tag']]
        if 'ko' in patch_item and patch_item['ko']:
            item['ko'] = patch_item['ko']
        if 'en' in patch_item and patch_item['en']:
            item['en'] = patch_item['en']
        patched_count += 1

with open(target_file, 'w', encoding='utf-8') as f:
    json.dump(target_data, f, indent=2, ensure_ascii=False)

print(f"Patched {patched_count} items from my transcript.")
