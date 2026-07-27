import glob
import os
import re

files = sorted(glob.glob('books/art_of_war/copyright_*.txt') + 
               glob.glob('books/seneca_on_happiness/copyright_*.txt') + 
               glob.glob('books/seneca_shortness_of_life/copyright_*.txt') + 
               glob.glob('books/thirty_six_stratagems/copyright_*.txt'))

ko_pattern = r"비평이나\s+서평에\s+인용된\s+짧은\s+발췌문\s+및\s+저작권법이\s+허용하는\s+특정\s+비상업적\s+용도를\s+제외하고,\s+본\s+출판물의\s+어떤\s+부분도\s+발행인의\s+사전\s+서면\s+허가\s+없이\s+복사,\s+녹음,\s+기타\s+전자적\s+또는\s+기계적\s+방법을\s+포함하여\s+어떠한\s+형태나\s+수단으로도\s+복제,\s+배포\s+또는\s+전송될\s+수\s+없습니다\."
en_pattern = r"No\s+part\s+of\s+this\s+publication\s+may\s+be\s+reproduced,\s+distributed,\s+or\s+transmitted\s+in\s+any\s+form\s+or\s+by\s+any\s+means,\s+including\s+photocopying,\s+recording,\s+or\s+other\s+electronic\s+or\s+mechanical\s+methods,\s+without\s+the\s+prior\s+written\s+permission\s+of\s+the\s+publisher,\s+except\s+in\s+the\s+case\s+of\s+brief\s+quotations\s+embodied\s+in\s+critical\s+reviews\s+and\s+certain\s+noncommercial\s+uses\s+permitted\s+by\s+copyright\s+law\."

for f in files:
    print(f"Processing {f}...")
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_len = len(content)
    
    # Remove the target patterns
    content = re.sub(ko_pattern, "", content)
    content = re.sub(en_pattern, "", content)
    
    # Clean up double blank lines that may result from removing a paragraph
    content = re.sub(r'\n{3,}', '\n\n', content)
    # Strip leading/trailing whitespaces
    content = content.strip() + "\n"
    
    if len(content) < original_len:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"  Successfully cleaned! Removed restriction paragraph.")
    else:
        print(f"  No matching restriction paragraph found (or already cleaned).")
