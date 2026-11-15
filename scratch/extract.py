import json

tags = ['P004_4', 'P005_1', 'P007_1', 'P007_2', 'P009_1', 'P010_3', 'P010_4', 'P010_5', 'P011_2', 'P011_4', 'P012_1', 'P012_3', 'P014_3', 'P015_2', 'P015_3', 'P017_1', 'P019_1', 'P019_2', 'P027_2', 'P027_4', 'P031_2', 'P032_1', 'P033', 'P034_1', 'P039_1', 'P040_2', 'P041_1', 'P041_3', 'P042_2', 'P043_3', 'P045_1', 'P045_2', 'P045_4', 'P050_1', 'P050_2', 'P051_1', 'P053_2', 'P057_1', 'P057_2', 'P057_3', 'P058', 'P059', 'P060_1', 'P060_2', 'P065_1', 'P066', 'P067_1', 'P068_2', 'P072_2', 'P073_2', 'P074', 'P075_1', 'P075_2', 'P076', 'P077_1', 'P077_2', 'P077_4', 'P078_3']

with open('c:/git_repo/TKprof_book/books/two_cities/json/book2_ch_21.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('c:/git_repo/TKprof_book/scratch/read_tags.txt', 'w', encoding='utf-8') as out:
    for block in data:
        if block['tag'] in tags:
            out.write(f"TAG: {block['tag']}\n")
            out.write(f"RAW: {block['raw']}\n")
            out.write('-'*40 + '\n')
