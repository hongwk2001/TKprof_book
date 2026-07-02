import json
import glob

# Allow list
known_good = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:\'"-—()’“”\n\r\t')
special_chars = set()

for file in glob.glob('scripts/script_ch_*.json'):
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            text = item.get('text', '')
            for char in text:
                if char not in known_good:
                    special_chars.add(char)

print('Special chars:', repr(''.join(special_chars)))
