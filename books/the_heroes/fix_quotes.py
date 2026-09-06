import glob
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_PATH = os.path.join(BASE_DIR, "the_heroes_raw.json")

def clean_quotes():
    quote_chars = "\"\'“”‘’`"
    total_cleaned = 0

    for ch_path in sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json"))):
        changed = False
        with open(ch_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        for it in items:
            for s in it.get("translation", []):
                for lang in ["en", "kr"]:
                    val = s.get(lang, "")
                    cleaned = val.strip(quote_chars)
                    if val != cleaned:
                        print(f"[{os.path.basename(ch_path)}] Block {it['id']} Sent {s['id']} [{lang}]: {val!r} -> {cleaned!r}")
                        s[lang] = cleaned
                        changed = True
                        total_cleaned += 1

        if changed:
            with open(ch_path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)

    # Sync master JSON
    if os.path.exists(MASTER_PATH):
        with open(MASTER_PATH, "r", encoding="utf-8") as mf:
            master = json.load(mf)
        for ch in master.get("chapters", []):
            ch_json_file = os.path.join(JSON_DIR, f"{ch['chapter_id']}.json")
            if os.path.exists(ch_json_file):
                with open(ch_json_file, "r", encoding="utf-8") as cf:
                    ch["paragraphs"] = json.load(cf)
        with open(MASTER_PATH, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)

    print(f"Total outer quotes cleaned: {total_cleaned}")

if __name__ == "__main__":
    clean_quotes()
