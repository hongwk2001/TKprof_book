import json
import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for item in data:
        text = item.get('text', '')
        for old_str, new_str in replacements.items():
            if old_str in text:
                text = text.replace(old_str, new_str)
                item['text'] = text
                
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {filepath}")

# script_ch_04.json: Replace "Bah!" with "Ugh!".
replace_in_file('scripts/script_ch_04.json', {'Bah!': 'Ugh!'})

# script_ch_06.json: Replace "Behold," with "Look at that,".
replace_in_file('scripts/script_ch_06.json', {'Behold,': 'Look at that,'})

# script_ch_08.json: Replace "Alas," with "Unfortunately,".
replace_in_file('scripts/script_ch_08.json', {'Alas,': 'Unfortunately,'})

# script_ch_11.json: Replace "Bah!" with "Bullcrap!". and "'Behold!'" with "'Look!'".
replace_in_file('scripts/script_ch_11.json', {
    'Bah!': 'Bullcrap!',
    "'Behold!'": "'Look!'"
})
