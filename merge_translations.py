import json
import os
import re
import codecs

log_file = r'C:\Users\hongw\.gemini\antigravity\brain\3d8fad39-b55e-47b1-a202-33319a5742d6\.system_generated\logs\transcript.jsonl'
lines = codecs.open(log_file, 'r', 'utf-8').readlines()
translated_blocks = {}

for line in lines:
    if '"tag"' in line and '"en"' in line and '"ko"' in line:
        try:
            # find all JSON arrays in the line
            matches = re.findall(r'\[\s*\{\s*\\"tag\\":.*?\]', line)
            for m in matches:
                # The line is a JSON string, so the inner JSON might be escaped
                # Let's unescape it first or just parse the whole line as JSON and extract
                pass
            
            event = json.loads(line)
            # Dump the event dict to a string and look for the array
            event_str = json.dumps(event)
            matches = re.findall(r'(\[\s*\{\s*"tag"\s*:\s*"[^"]+",\s*"en"\s*:\s*".*?\])', event_str)
            for m in matches:
                arr = json.loads(m)
                for item in arr:
                    translated_blocks[item['tag']] = item
        except Exception as e:
            pass

print('Found using basic regex:', len(translated_blocks))

# Another approach: just scan the raw line for the substring
for line in lines:
    try:
        event = json.loads(line)
        if 'content' in event:
            content = event['content']
            if isinstance(content, str) and '"tag"' in content and '"en"' in content:
                # try to parse content as JSON
                try:
                    arr = json.loads(content)
                    if isinstance(arr, list):
                        for item in arr:
                            if 'tag' in item and 'en' in item:
                                translated_blocks[item['tag']] = item
                except:
                    # Maybe it has some prefix text
                    match = re.search(r'\[\s*\{\s*"tag":.*\]', content, re.DOTALL)
                    if match:
                        arr = json.loads(match.group(0))
                        for item in arr:
                            translated_blocks[item['tag']] = item
        # also check system messages
        if event.get('type') == 'systemMessage' or event.get('type') == 'message':
            pass
    except Exception as e:
        pass

print('Found translated items:', len(translated_blocks))

original_file = r'c:\git_repo\TKprof_book\books\two_cities\json\book1_ch_02.json'
data = json.load(codecs.open(original_file, 'r', 'utf-8-sig'))

updated = 0
for b in data:
    tag = b.get('tag')
    if tag in translated_blocks:
        b['en'] = translated_blocks[tag].get('en', '')
        b['ko'] = translated_blocks[tag].get('ko', '')
        updated += 1

print('Updated items in memory:', updated)
codecs.open(original_file, 'w', 'utf-8').write(json.dumps(data, ensure_ascii=False, indent=2))
print('Saved to file.')
