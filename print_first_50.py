import json
import codecs
with codecs.open('c:/git_repo/TKprof_book/scratch_en.json', 'r', 'utf-8') as f:
    d = json.load(f)

for i in range(50):
    print(f"{d[i]['id']} | {d[i]['target_en']}")
