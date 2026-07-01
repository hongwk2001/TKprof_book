import json
import glob
import os

def fix_scripts():
    for file in sorted(glob.glob('scripts/script_ch_*.json')):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        basename = os.path.basename(file)
        ch_num = int(basename.replace('script_ch_', '').replace('.json', ''))
        
        # 1. Strip special characters
        for item in data:
            item['text'] = item['text'].replace('*', '').replace('#', '')
            
        # 2. Prepend Chapter X to title for chapters 3-11
        if 3 <= ch_num <= 11:
            first_text = data[0]['text']
            if not first_text.startswith(f"Chapter {ch_num}:"):
                # The title might be multi-line or just the first line. 
                # Let's prepend it simply.
                data[0]['text'] = f"Chapter {ch_num}: {first_text}"
                
        # 3. Append End announcement to Chapter 11
        if ch_num == 11:
            last_text = data[-1]['text']
            end_msg = "End of The Richest Man in Babylon."
            if end_msg not in last_text:
                data[-1]['text'] = last_text + f"\n\n{end_msg}"
                
        # Save back
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"Processed {file}")

if __name__ == '__main__':
    fix_scripts()
