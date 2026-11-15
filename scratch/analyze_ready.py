import os
import sys
sys.path.append(r"C:\git_repo\TKprof_book")
import json
from check_audio_quality import check_file

dir_path = r"C:\git_repo\TKprof_book\books\blue_castle\final_audio_ko_ready"
files = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.endswith(".mp3")]

passed = 0
failed = 0
results = []
for f in sorted(files):
    res = check_file(f)
    results.append(res)
    if res["status"] == "PASS":
        passed += 1
    else:
        failed += 1

print(f"final_audio_ko_ready: {passed} PASSED, {failed} FAILED out of {len(results)} files.")
