import os
import sys
sys.path.append(r"C:\git_repo\TKprof_book")
import json
from check_audio_quality import check_file

dir_path = r"C:\git_repo\TKprof_book\books\blue_castle\final_audio_ko"
files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".mp3")]

results = []
for f in sorted(files):
    res = check_file(f)
    results.append(res)

with open(r"C:\git_repo\TKprof_book\scratch\audit_results.json", "w", encoding="utf-8") as out:
    json.dump(results, out, indent=2)

print(f"Audited {len(results)} files.")
