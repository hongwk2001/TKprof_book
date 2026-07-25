import os
import re

input_dir = r"d:\git_repo\TKprof_book\books\the_enchanted_april\chapters"
output_dir = os.path.join(input_dir, "tagged")
os.makedirs(output_dir, exist_ok=True)

lotty_names = ["윌킨스", "로티", "Lotty", "Wilkins"]
rose_names = ["아버스넛", "로즈", "Rose", "Arbuthnot"]
other_names = ["스크랩", "캐롤라인", "피셔", "멜러쉬", "브릭스", "토머스", "도메니코", "프란체스카", "아런델", "Scrap", "Caroline", "Fisher", "Mellersh", "Briggs", "거스루드", "코스트라", "프레더릭"]

def identify_speaker(text, prev_speaker, prev_prev_speaker):
    speech_verbs = ["말했", "대답했", "물었", "중얼거렸", "소리쳤", "덧붙였", "물어보았", "되물었", "지적했", "외쳤"]
    verb_pattern = "|".join(speech_verbs)
    
    lotty_pattern = "|".join(lotty_names)
    rose_pattern = "|".join(rose_names)
    other_pattern = "|".join(other_names)
    
    def get_closest_match(pattern):
        matches = list(re.finditer(f"({pattern}).*?({verb_pattern})", text))
        return matches
        
    lotty_matches = get_closest_match(lotty_pattern)
    rose_matches = get_closest_match(rose_pattern)
    other_matches = get_closest_match(other_pattern)
    
    if lotty_matches or rose_matches or other_matches:
        all_matches = []
        if lotty_matches: all_matches.append((lotty_matches[0].start(), "Lotty"))
        if rose_matches: all_matches.append((rose_matches[0].start(), "Rose"))
        if other_matches: all_matches.append((other_matches[0].start(), "Other"))
        if all_matches:
            all_matches.sort(key=lambda x: x[0])
            return all_matches[0][1]

    has_lotty = any(name in text for name in lotty_names)
    has_rose = any(name in text for name in rose_names)
    has_other = any(name in text for name in other_names)
    
    if has_lotty and not has_rose and not has_other: return "Lotty"
    if has_rose and not has_lotty and not has_other: return "Rose"
    if has_other and not has_lotty and not has_rose: return "Other"
    
    if prev_speaker and prev_prev_speaker:
        if prev_speaker != prev_prev_speaker and not (has_lotty and has_rose and has_other):
            if has_lotty and prev_prev_speaker == "Lotty": return "Lotty"
            if has_rose and prev_prev_speaker == "Rose": return "Rose"
            if has_other and prev_prev_speaker == "Other": return "Other"
            if not has_lotty and not has_rose and not has_other:
                return prev_prev_speaker
    
    if prev_speaker == "Lotty":
        return "Rose" if has_rose else "Other"
    elif prev_speaker == "Rose":
        return "Lotty" if has_lotty else "Other"
        
    return "Other"

def process_file(filename):
    filepath = os.path.join(input_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    paragraphs = content.split('\n')
    new_paragraphs = []
    
    prev_speaker = None
    prev_prev_speaker = None
    
    for p in paragraphs:
        if '"' in p or '“' in p or '”' in p:
            speaker = identify_speaker(p, prev_speaker, prev_prev_speaker)
            
            def replacer(match):
                q = match.group(0)
                if len(q) > 3:
                    return f"<{speaker}>{q}</{speaker}>"
                return q
            
            new_p = re.sub(r'("[^"]+")', replacer, p)
            new_p = re.sub(r'(“[^”]+”)', replacer, new_p)
            
            if ("<" + speaker + ">") in new_p:
                prev_prev_speaker = prev_speaker
                prev_speaker = speaker
            
            new_paragraphs.append(new_p)
        else:
            new_paragraphs.append(p)
            
    out_filepath = os.path.join(output_dir, "tagged_" + filename)
    with open(out_filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(new_paragraphs))
        
    print(f"Processed {filename}")

for i in range(12, 23):
    try:
        process_file(f"ch_{i}_ko.txt")
    except FileNotFoundError:
        print(f"ch_{i}_ko.txt not found")
