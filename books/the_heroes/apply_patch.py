import os
import json
import glob

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
BATCHES_DIR = os.path.join(BASE_DIR, "batches")
MASTER_JSON = os.path.join(BASE_DIR, "the_heroes_raw.json")

def apply_patch():
    batch_files = sorted(glob.glob(os.path.join(BATCHES_DIR, "*.json")))
    if not batch_files:
        print(f"No batch files found in {BATCHES_DIR}.")
        return

    # Patches keyed by paragraph block id
    full_translation_patches = {}
    en_patches = {}
    kr_patches = {}

    for bf in batch_files:
        try:
            with open(bf, "r", encoding="utf-8") as f:
                data = json.load(f)
            items = data if isinstance(data, list) else data.get("items", [])
            for it in items:
                b_id = it.get("id")
                if not b_id:
                    continue

                # Case 1: Unified translation array provided
                if "translation" in it and isinstance(it["translation"], list) and len(it["translation"]) > 0:
                    full_translation_patches[b_id] = it["translation"]
                    for s in it["translation"]:
                        s_id = s.get("id")
                        if "en" in s and s["en"].strip():
                            en_patches.setdefault(b_id, {})[s_id] = s["en"].strip()
                        if "kr" in s and s["kr"].strip():
                            kr_patches.setdefault(b_id, {})[s_id] = s["kr"].strip()

                # Case 2: Direct 'kr' list or dict provided
                if "kr" in it:
                    kr_val = it["kr"]
                    if isinstance(kr_val, list):
                        for idx, s in enumerate(kr_val, 1):
                            if isinstance(s, dict):
                                s_id = s.get("id", idx)
                                s_text = s.get("kr", s.get("text", "")).strip()
                            else:
                                s_id = idx
                                s_text = str(s).strip()
                            if s_text:
                                kr_patches.setdefault(b_id, {})[s_id] = s_text
                    elif isinstance(kr_val, dict):
                        for k, v in kr_val.items():
                            kr_patches.setdefault(b_id, {})[int(k)] = str(v).strip()

                # Case 3: Direct 'en' list or dict provided
                if "en" in it and not isinstance(it.get("translation"), list):
                    en_val = it["en"]
                    if isinstance(en_val, list):
                        for idx, s in enumerate(en_val, 1):
                            if isinstance(s, dict):
                                s_id = s.get("id", idx)
                                s_text = s.get("en", s.get("text", "")).strip()
                            else:
                                s_id = idx
                                s_text = str(s).strip()
                            if s_text:
                                en_patches.setdefault(b_id, {})[s_id] = s_text

            print(f"Loaded batch {os.path.basename(bf)} ({len(items)} items)")
        except Exception as e:
            print(f"Error reading {bf}: {e}")

    print(f"Total blocks with EN patches: {len(en_patches)}, KR patches: {len(kr_patches)}")

    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    total_updated_blocks = 0

    for ch_path in ch_files:
        with open(ch_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        ch_changed = False
        for it in items:
            b_id = it["id"]

            # If full translation provided and current translation is empty or being replaced:
            if b_id in full_translation_patches:
                it["translation"] = full_translation_patches[b_id]
                ch_changed = True
                total_updated_blocks += 1
                continue

            translations = it.setdefault("translation", [])

            # Apply EN patches
            if b_id in en_patches:
                patch_map = en_patches[b_id]
                for s in translations:
                    s_id = s["id"]
                    if s_id in patch_map:
                        s["en"] = patch_map[s_id]
                        ch_changed = True

            # Apply KR patches
            if b_id in kr_patches:
                patch_map = kr_patches[b_id]
                for s in translations:
                    s_id = s["id"]
                    if s_id in patch_map:
                        s["kr"] = patch_map[s_id]
                        ch_changed = True

            if b_id in en_patches or b_id in kr_patches:
                total_updated_blocks += 1

        if ch_changed:
            with open(ch_path, "w", encoding="utf-8") as f:
                json.dump(items, f, ensure_ascii=False, indent=2)
            print(f"Updated {os.path.basename(ch_path)} with patches.")

    # Update Master JSON
    if os.path.exists(MASTER_JSON):
        with open(MASTER_JSON, "r", encoding="utf-8") as mf:
            master = json.load(mf)

        for ch in master.get("chapters", []):
            ch_id = ch["chapter_id"]
            ch_json_file = os.path.join(JSON_DIR, f"{ch_id}.json")
            if os.path.exists(ch_json_file):
                with open(ch_json_file, "r", encoding="utf-8") as f:
                    ch["paragraphs"] = json.load(f)

        with open(MASTER_JSON, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)

    print(f"Successfully applied patches across {total_updated_blocks} blocks.")

if __name__ == "__main__":
    apply_patch()
