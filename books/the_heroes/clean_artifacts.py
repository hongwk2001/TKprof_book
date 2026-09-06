import os
import sys
import glob
import json
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_PATH = os.path.join(BASE_DIR, "the_heroes_raw.json")

def should_purge(block):
    raw = block.get("raw", "").strip()
    
    # 1. Asterism dividers
    if raw == "* * * * *" or re.fullmatch(r'[\*\s]+', raw):
        return True
        
    # 2. Publisher colophons
    if "Printed by" in raw and "Edinburgh" in raw:
        return True
        
    # 3. Footnotes header
    if raw == "Footnotes":
        return True
        
    # 4. Isolated Gutenberg footnotes e.g. {96} In the Elgin Marbles.
    if re.match(r'^\{\d+[a-z]?\}', raw):
        return True
        
    return False

def clean_and_renumber():
    ch_files = sorted(glob.glob(os.path.join(JSON_DIR, "ch_*.json")))
    
    purged_blocks = []
    total_original_blocks = 0
    cleaned_chapters = {}
    
    global_id = 1
    
    for ch_path in ch_files:
        ch_name = os.path.basename(ch_path)
        with open(ch_path, "r", encoding="utf-8") as f:
            blocks = json.load(f)
            
        kept_blocks = []
        for b in blocks:
            total_original_blocks += 1
            if should_purge(b):
                purged_blocks.append({
                    "chapter": ch_name,
                    "id": b["id"],
                    "tag": b.get("tag"),
                    "raw": b.get("raw")
                })
            else:
                # Renumber
                b["id"] = global_id
                b["tag"] = f"P{global_id:04d}"
                global_id += 1
                kept_blocks.append(b)
                
        cleaned_chapters[ch_path] = kept_blocks

    print(f"Total Original Blocks: {total_original_blocks}")
    print(f"Purged Blocks:         {len(purged_blocks)}")
    print(f"Remaining Blocks:      {global_id - 1}\n")
    
    print("Purged Items Detail:")
    for p in purged_blocks:
        print(f"  [{p['chapter']}] Block {p['id']} ({p['tag']}): {p['raw']!r}")
    print()

    # Save cleaned chapter files
    for ch_path, blocks in cleaned_chapters.items():
        with open(ch_path, "w", encoding="utf-8") as f:
            json.dump(blocks, f, ensure_ascii=False, indent=2)
        print(f"Saved {os.path.basename(ch_path)} ({len(blocks)} blocks)")

    # Update Master JSON
    if os.path.exists(MASTER_PATH):
        with open(MASTER_PATH, "r", encoding="utf-8") as mf:
            master = json.load(mf)
            
        total_master_blocks = 0
        for ch in master.get("chapters", []):
            ch_id = ch["chapter_id"]
            ch_file = os.path.join(JSON_DIR, f"{ch_id}.json")
            if os.path.exists(ch_file):
                with open(ch_file, "r", encoding="utf-8") as cf:
                    updated_paras = json.load(cf)
                ch["paragraphs"] = updated_paras
                ch["paragraph_count"] = len(updated_paras)
                total_master_blocks += len(updated_paras)
                
        master["total_paragraphs"] = total_master_blocks
        
        with open(MASTER_PATH, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)
        print(f"\nMaster JSON synchronized ({total_master_blocks} total blocks).")

if __name__ == "__main__":
    clean_and_renumber()
