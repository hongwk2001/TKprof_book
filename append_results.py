import json
import sys
import os

results_file = 'c:/git_repo/TKprof_book/all_results.json'
new_data_file = sys.argv[1]

with open(new_data_file, 'r', encoding='utf-8') as f:
    try:
        new_data = json.load(f)
    except json.JSONDecodeError:
        print("Invalid JSON.")
        sys.exit(1)

if os.path.exists(results_file):
    with open(results_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
else:
    all_data = []

all_data.extend(new_data)

with open(results_file, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, indent=2, ensure_ascii=False)

print(f"Appended {len(new_data)} items. Total: {len(all_data)}")
