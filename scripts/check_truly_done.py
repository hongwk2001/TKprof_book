import json
import glob
import os

JSON_DIR = 'c:/git_repo/TKprof_book/books/two_cities/json'
files = sorted(glob.glob(os.path.join(JSON_DIR, 'book*_ch_*.json')))

truly_incomplete = []
complete = []

for f in files:
    name = os.path.basename(f)
    if os.path.getsize(f) == 0:
        truly_incomplete.append((name, 'EMPTY FILE', 0))
        continue
    try:
        data = json.load(open(f, encoding='utf-8'))
    except UnicodeDecodeError:
        data = json.load(open(f, encoding='utf-16'))
    except Exception as e:
        truly_incomplete.append((name, f'ERROR: {e}', 0))
        continue

    if not isinstance(data, list):
        continue

    missing = [b for b in data if isinstance(b, dict)
               and not b.get('is_header')
               and (not b.get('en', '').strip() or not b.get('ko', '').strip())]

    if missing:
        truly_incomplete.append((name, len(missing), len(data)))
    else:
        complete.append(name)

print(f'TRULY COMPLETE (non-header blocks all filled): {len(complete)}/45')
for c in complete:
    print(f'  {c}')

print(f'\nSTILL NEEDS WORK: {len(truly_incomplete)}/45')
for name, miss, total in truly_incomplete:
    print(f'  {name}: {miss} non-header blocks missing')
