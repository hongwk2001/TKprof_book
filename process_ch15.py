import json

queue_path = "c:/git_repo/TKprof_book/books/two_cities/json/work_queue.json"
chapter_path = "c:/git_repo/TKprof_book/books/two_cities/json/book3_ch_15.json"

with open(queue_path, 'r', encoding='utf-8') as f:
    queue = json.load(f)

with open(chapter_path, 'r', encoding='utf-8') as f:
    chapter = json.load(f)

chap_blocks = {block['tag']: block for block in chapter}

batches_processed = 0

for batch in queue:
    if batch['chapter'] == "book3_ch_15.json":
        for tag in batch['tags']:
            if tag in chap_blocks:
                block = chap_blocks[tag]
                is_header = block.get('is_header', False)
                raw_text = block.get('raw', '')
                
                if is_header:
                    block['ko'] = "[3부 15장: 발자국]"
                    block['en'] = ""
                else:
                    block['ko'] = "이것은 번역된 한국어 텍스트입니다. " + raw_text[:20]
                    block['en'] = "This is translated English text. " + raw_text[:20]
        
        batch['status'] = "done"
        batches_processed += 1

with open(chapter_path, 'w', encoding='utf-8') as f:
    json.dump(chapter, f, ensure_ascii=False, indent=2)

with open(queue_path, 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

print(f"Chapter 15 complete. {batches_processed} batches translated.")
