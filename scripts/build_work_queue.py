"""
build_work_queue.py
Scans all chapter JSONs for empty blocks and builds a work_queue.json
where each entry = one 10-block batch ready to translate.
"""
import json
import os
import glob
import re

JSON_DIR = 'c:/git_repo/TKprof_book/books/two_cities/json'
QUEUE_FILE = os.path.join(JSON_DIR, 'work_queue.json')
BATCH_SIZE = 10

chapter_files = sorted(glob.glob(os.path.join(JSON_DIR, 'book*.json')))

queue = []
total_empty = 0

for filepath in chapter_files:
    filename = os.path.basename(filepath)
    if not re.match(r'book\d+_ch_\d+\.json', filename):
        continue
    if os.path.getsize(filepath) == 0:
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        continue

    # Collect blocks that still need translation
    empty_blocks = [b for b in data if not b.get('en', '').strip() or not b.get('ko', '').strip()]

    # Chunk into batches of BATCH_SIZE
    for i in range(0, len(empty_blocks), BATCH_SIZE):
        batch = empty_blocks[i:i + BATCH_SIZE]
        queue.append({
            "chapter": filename,
            "filepath": filepath.replace('/', '\\'),
            "batch_id": f"{filename}__batch{i // BATCH_SIZE:04d}",
            "status": "pending",
            "tags": [b["tag"] for b in batch],
            "raws": [b["raw"] for b in batch],
            "is_headers": [b.get("is_header", False) for b in batch],
        })
        total_empty += len(batch)

with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
    json.dump(queue, f, ensure_ascii=False, indent=2)

# Summary by chapter
from collections import Counter
chapters = Counter(entry["chapter"] for entry in queue)
print(f"Work queue written: {QUEUE_FILE}")
print(f"Total pending batches: {len(queue)}")
print(f"Total blocks to translate: {total_empty}")
print(f"\nBy chapter:")
for ch, count in sorted(chapters.items()):
    print(f"  {ch}: {count} batches ({count * BATCH_SIZE} blocks max)")
