import os
import re

input_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
output_dir = os.path.join(input_dir, "tagged")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

lotty_keywords = ["로티", "윌킨스"]
rose_keywords = ["로즈", "아버스넛"]

def tag_dialogue(text):
    paragraphs = text.split('\n')
    tagged_paragraphs = []
    
    last_speaker = "Other"
    
    # Matching double quotes or Korean style quotes
    pattern = re.compile(r'([“"「].*?[”"」])')
    
    for p in paragraphs:
        if not p.strip():
            tagged_paragraphs.append(p)
            continue
            
        quotes = pattern.findall(p)
        if not quotes:
            tagged_paragraphs.append(p)
            continue
            
        # Check current paragraph
        is_lotty = any(k in p for k in lotty_keywords)
        is_rose = any(k in p for k in rose_keywords)
        
        if is_lotty and not is_rose:
            current_speaker = "Lotty"
        elif is_rose and not is_lotty:
            current_speaker = "Rose"
        elif not is_lotty and not is_rose:
            if last_speaker == "Lotty":
                current_speaker = "Rose"
            elif last_speaker == "Rose":
                current_speaker = "Lotty"
            else:
                current_speaker = "Other"
        else:
            current_speaker = "Other"
            
        last_speaker = current_speaker
        
        def replace_quote(match):
            quote = match.group(0)
            return f"<{current_speaker}>{quote}</{current_speaker}>"

        new_p = pattern.sub(replace_quote, p)
        tagged_paragraphs.append(new_p)

    return '\n'.join(tagged_paragraphs)

processed_files = []
for i in range(1, 12):
    filename = f"ch_{i:02d}_ko.txt"
    filepath = os.path.join(input_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tagged = tag_dialogue(content)
        outpath = os.path.join(output_dir, f"tagged_{filename}")
        with open(outpath, 'w', encoding='utf-8') as f:
            f.write(tagged)
        processed_files.append(filename)

print("Processed:", ", ".join(processed_files))
