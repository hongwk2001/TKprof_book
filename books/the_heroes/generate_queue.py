import os
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
QUEUE_FILE = os.path.join(BASE_DIR, "work_queue.json")

def generate_queue():
    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    pending_items = []

    for fpath in ch_files:
        with open(fpath, "r", encoding="utf-8") as f:
            items = json.load(f)
        for it in items:
            if not it.get("en") or it.get("en").strip() == "":
                pending_items.append({
                    "id": it["id"],
                    "tag": it["tag"],
                    "chapter_id": it["chapter_id"],
                    "is_header": it["is_header"],
                    "raw": it["raw"]
                })

    with open(QUEUE_FILE, "w", encoding="utf-8") as qf:
        json.dump(pending_items, qf, ensure_ascii=False, indent=2)

    print(f"Queue generated at {QUEUE_FILE}: {len(pending_items)} pending items.")
    return pending_items

if __name__ == "__main__":
    generate_queue()
