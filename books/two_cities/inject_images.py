import os

mappings = [
    ("0403m", "book1_ch_01_en.txt", "CHAPTER I"),
    ("0404m", "book1_ch_01_en.txt", "It was the best of times"),
    ("0414m", "book1_ch_02_en.txt", "hallo you!"),
    ("0442m", "book1_ch_06_en.txt", "fell to work at his shoemaking"),
    ("0465m", "book2_ch_03_en.txt", "without trial"),
    ("0471m", "book2_ch_03_en.txt", "blue-flies"),
    ("0496m", "book2_ch_07_en.txt", "reared and plunged"),
    ("0524m", "book2_ch_12_en.txt", "eligible"),
    ("0535m", "book2_ch_14_en.txt", "procession"),
    ("0544m", "book2_ch_15_en.txt", "entered the wine-shop"),
    ("0576m", "book2_ch_18_en.txt", "horrible crime"),
    ("0592m", "book2_ch_22_en.txt", "rousing the women"),
    ("0616m", "book3_ch_01_en.txt", "without delay"),
    ("0649m", "book3_ch_07_en.txt", "red caps"),
    ("0653m", "book3_ch_08_en.txt", "evidently English"),
    ("0686m", "book3_ch_11_en.txt", "fell at his feet"),
]

chapters_dir = 'd:/git_repo/TKprof_book/books/two_cities/chapters/'

for img_id, ch_file, search_text in mappings:
    path = os.path.join(chapters_dir, ch_file)
    if not os.path.exists(path):
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    img_md = f"![illustration](images/{img_id}_color.png)"
    if img_md in content:
        continue
        
    paras = content.split('\n\n')
    new_paras = []
    injected = False
    for p in paras:
        if not injected and search_text.lower() in p.lower():
            new_paras.append(p)
            new_paras.append(img_md)
            injected = True
        else:
            new_paras.append(p)
            
    if not injected:
        # Fallback: just append to the end of the chapter!
        new_paras.append(img_md)
        print(f"Appended {img_id} to END of {ch_file}")
    else:
        print(f"Injected {img_id} inline in {ch_file}")
        
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(new_paras))
        
print("Done!")
