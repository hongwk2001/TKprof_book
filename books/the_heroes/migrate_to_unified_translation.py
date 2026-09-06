import os
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_JSON = os.path.join(BASE_DIR, "the_heroes_raw.json")

def migrate_item(item):
    new_item = {
        "id": item["id"],
        "tag": item["tag"],
        "chapter_id": item["chapter_id"],
        "story": item["story"],
        "part": item["part"],
        "raw": item["raw"],
        "is_header": item["is_header"],
        "word_count": item["word_count"],
        "translation": []
    }

    # If item has old 'en' field
    old_en = item.get("en")
    if isinstance(old_en, list) and old_en:
        for s in old_en:
            new_item["translation"].append({
                "id": s["id"],
                "en": s.get("text", s.get("en", "")),
                "kr": s.get("kr", "")
            })
    elif isinstance(old_en, str) and old_en.strip():
        new_item["translation"].append({
            "id": 1,
            "en": old_en.strip(),
            "kr": ""
        })

    return new_item

def migrate_all():
    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    total_migrated_sentences = 0

    for ch_path in ch_files:
        with open(ch_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        migrated_items = [migrate_item(it) for it in items]
        s_count = sum(len(it["translation"]) for it in migrated_items)
        total_migrated_sentences += s_count

        with open(ch_path, "w", encoding="utf-8") as f:
            json.dump(migrated_items, f, ensure_ascii=False, indent=2)

        print(f"Migrated {os.path.basename(ch_path)}: {len(migrated_items)} blocks, {s_count} translation items.")

    # Migrate Master JSON
    if os.path.exists(MASTER_JSON):
        with open(MASTER_JSON, "r", encoding="utf-8") as mf:
            master = json.load(mf)

        for ch in master.get("chapters", []):
            ch_id = ch["chapter_id"]
            ch_file = os.path.join(JSON_DIR, f"{ch_id}.json")
            if os.path.exists(ch_file):
                with open(ch_file, "r", encoding="utf-8") as cf:
                    ch["paragraphs"] = json.load(cf)

        with open(MASTER_JSON, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)
        print(f"Migrated Master JSON: {MASTER_JSON}")

    print(f"\nMigration complete! Total paired sentence objects: {total_migrated_sentences}")

if __name__ == "__main__":
    migrate_all()
