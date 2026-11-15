import json
import glob
import os
import re

JSON_DIR = 'c:/git_repo/TKprof_book/books/two_cities/json'
QUEUE_FILE = os.path.join(JSON_DIR, 'work_queue.json')

# Check queue status
try:
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    done = sum(1 for q in queue if q.get('status') == 'done')
    pending = sum(1 for q in queue if q.get('status') == 'pending')
    print(f"Work queue: {done} done / {pending} pending / {len(queue)} total batches")
except Exception as e:
    print(f"Queue error: {e}")

print()

# Check chapter files
chapter_files = sorted(glob.glob(os.path.join(JSON_DIR, 'book*_ch_*.json')))
skip = {'book2_ch_19_updated.json', 'book2_ch_11_empty.json', 'book2_ch_11_batches.json'}

complete = []
incomplete = []

for filepath in chapter_files:
    name = os.path.basename(filepath)
    if name in skip:
        continue
    if not re.match(r'book\d+_ch_\d+\.json', name):
        continue
    if os.path.getsize(filepath) == 0:
        incomplete.append(f"  {name}: EMPTY FILE")
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        incomplete.append(f"  {name}: JSON ERROR - {e}")
        continue

    total = len(data)
    missing = sum(1 for b in data if not b.get('en', '').strip() or not b.get('ko', '').strip())
    if missing == 0:
        complete.append(f"  {name}: {total}/{total} done")
    else:
        incomplete.append(f"  {name}: {total - missing}/{total} done ({missing} missing)")

print(f"COMPLETE ({len(complete)}/45 chapters):")
for c in complete:
    print(c)

print(f"\nINCOMPLETE ({len(incomplete)}/45 chapters):")
for i in incomplete:
    print(i)
