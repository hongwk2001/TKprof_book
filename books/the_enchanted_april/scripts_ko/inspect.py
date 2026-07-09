import json
import codecs

with codecs.open('inspect.txt', 'w', encoding='utf-8') as out:
    for ch in [17, 18, 19, 21]:
        with open(f'd:/git_repo/TKprof_book/books/the_enchanted_april/scripts_ko/script_ch_{ch}.json', encoding='utf-8') as f:
            data = json.load(f)
        out.write(f'--- Chapter {ch} ---\n')
        for i, item in enumerate(data):
            out.write(f'{i}: {item["character"]} - {repr(item["text"])}\n')
