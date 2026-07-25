import os
import glob
import re

def process_file(filepath, outpath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # We will identify speakers based on mentions in the surrounding paragraph.
    def replacer(match):
        dialogue = match.group(0)
        start_idx = text.rfind('\n', 0, match.start())
        end_idx = text.find('\n', match.end())
        if start_idx == -1: start_idx = 0
        if end_idx == -1: end_idx = len(text)
        paragraph = text[start_idx:end_idx]

        lotty_score = len(re.findall(r'\b(Lotty|Mrs\. Wilkins|Wilkins)\b', paragraph))
        rose_score = len(re.findall(r'\b(Rose|Mrs\. Arbuthnot|Arbuthnot)\b', paragraph))
        other_score = len(re.findall(r'\b(Scrap|Lady Caroline|Caroline|Mrs\. Fisher|Fisher|Mellersh|Thomas|Briggs|Domenico|Francesca|Browning)\b', paragraph))

        # Assign tag
        if lotty_score > rose_score and lotty_score > other_score:
            tag = "Lotty"
        elif rose_score > lotty_score and rose_score > other_score:
            tag = "Rose"
        else:
            tag = "Other"
            
        return f"<{tag}>{dialogue}</{tag}>"

    # Regex to find quotes (both regular and smart quotes)
    # This regex ensures we only wrap the quote itself.
    # It handles “...”, "...", etc.
    # To handle multi-paragraph we should just wrap any sequence of quotes.
    # For simplicity, we wrap “something” and "something"
    new_text = re.sub(r'([“"])(.*?)(["”])', replacer, text, flags=re.DOTALL)
    
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(new_text)

os.makedirs('tagged', exist_ok=True)
for i in range(12, 23):
    fname = f'ch_{i}_en.txt'
    if os.path.exists(fname):
        process_file(fname, f'tagged/tagged_{fname}')
        print(f'Processed {fname}')
