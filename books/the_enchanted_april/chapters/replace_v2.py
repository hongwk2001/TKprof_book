import os
import re

line_to_speaker = {
    15: "Other",
    25: "Lotty",
    31: "Other",
    49: "Lotty",
    55: "Rose",
    57: "Lotty",
    61: "Lotty",
    63: "Rose",
    65: "Lotty",
    69: "Lotty",
    77: "Rose",
    79: "Lotty",
    81: "Rose",
    83: "Lotty",
    85: "Rose",
    87: "Lotty",
    89: "Rose",
    91: "Lotty",
    93: "Rose",
    95: "Lotty",
    99: "Rose",
    101: "Lotty",
    105: "Other",
    113: "Lotty",
    115: "Rose",
    117: "Lotty",
    119: "Rose",
    129: "Lotty",
    131: "Rose",
    133: "Lotty",
    135: "Rose",
    137: "Lotty",
    139: "Rose",
    141: "Lotty",
    143: "Rose",
    145: "Lotty",
    147: "Rose",
    149: "Lotty",
    153: "Lotty",
    157: "Rose",
    159: "Lotty",
    161: "Rose",
    163: "Lotty",
    165: "Rose",
    167: "Lotty",
    181: "Rose",
    185: "Lotty",
    187: "Rose",
    189: "Lotty",
    191: "Rose",
    195: "Rose",
    197: "Lotty",
    199: "Rose",
    201: "Lotty",
    207: "Lotty",
    209: "Rose",
    211: "Lotty"
}

def process_file(in_path, out_path):
    with open(in_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for i, line in enumerate(lines, start=1):
        if i in line_to_speaker:
            speaker = line_to_speaker[i]
            
            # Special case for line 133 english: "'how wonderful'" is not double quotes. But there are double quotes. 
            # We want to replace double quotes.
            # Replace all occurrences of "..." with <Speaker>"..."</Speaker>
            
            # Find all double quote matches
            def repl(m):
                # Only wrap if it's not already wrapped (to prevent double wrap if we run it multiple times)
                # But since we read from original each time it's fine.
                return f"<{speaker}>{m.group(0)}</{speaker}>"
            
            line = re.sub(r'"([^"]*)"', repl, line)
        
        new_lines.append(line)
        
    with open(out_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

in_dir = r'd:\git_repo\TKprof_book\books\the_enchanted_april\chapters'
out_dir = os.path.join(in_dir, 'tagged')
os.makedirs(out_dir, exist_ok=True)

process_file(os.path.join(in_dir, 'ch_01_en.txt'), os.path.join(out_dir, 'ch_01_en.txt'))
process_file(os.path.join(in_dir, 'ch_01_ko.txt'), os.path.join(out_dir, 'ch_01_ko.txt'))

print('Files successfully tagged.')
