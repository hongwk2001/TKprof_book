import json
with open('c:/git_repo/TKprof_book/blocks_to_translate.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('c:/git_repo/TKprof_book/simple_blocks.txt', 'w', encoding='utf-8') as f:
    for idx, item in enumerate(data):
        f.write(f"[{idx+261}] ID:{item['id']}\n")
        f.write(f"RAW: {item['target_raw']}\n\n")
