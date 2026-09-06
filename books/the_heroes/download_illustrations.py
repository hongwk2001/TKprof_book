import os
import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
JSON_DIR = os.path.join(BASE_DIR, "json")
MASTER_PATH = os.path.join(BASE_DIR, "the_heroes_raw.json")

os.makedirs(IMAGES_DIR, exist_ok=True)

ILLUSTRATIONS = [
    {
        "url": "https://www.gutenberg.org/cache/epub/677/pg677.cover.medium.jpg",
        "filename": "cover.jpg",
        "chapter_id": None,
        "block_tag": None,
        "caption": "Book Cover"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p4b.jpg",
        "filename": "01_danae_and_baby.jpg",
        "chapter_id": "ch_01",
        "block_tag": "P0026",
        "caption": "Danae and her baby adrift in the chest"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p43b.jpg",
        "filename": "02_perseus_and_andromeda.jpg",
        "chapter_id": "ch_04",
        "block_tag": "P0182",
        "caption": "Perseus and the maid"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p70b.jpg",
        "filename": "03_chiron_the_centaur.jpg",
        "chapter_id": "ch_06",
        "block_tag": "P0292",
        "caption": "Chiron the Centaur"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p78b.jpg",
        "filename": "04_jason_and_hera.jpg",
        "chapter_id": "ch_07",
        "block_tag": "P0328",
        "caption": "Jason and Hera"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p124b.jpg",
        "filename": "05_jason_takes_fleece.jpg",
        "chapter_id": "ch_09",
        "block_tag": "P0480",
        "caption": "Jason takes the fleece"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p169b.jpg",
        "filename": "06_theseus_and_aithra.jpg",
        "chapter_id": "ch_12",
        "block_tag": "P0642",
        "caption": "Theseus and Aithra"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p212b.jpg",
        "filename": "07_theseus_and_minotaur.jpg",
        "chapter_id": "ch_14",
        "block_tag": "P0839",
        "caption": "Theseus and Minotaur"
    },
    {
        "url": "https://www.gutenberg.org/cache/epub/677/images/p217b.jpg",
        "filename": "08_warriors_fighting.jpg",
        "chapter_id": "ch_15",
        "block_tag": "P0850",
        "caption": "Warriors fighting"
    }
]

def download_and_link():
    print("=== Downloading Public Domain Illustrations ===\n")
    downloaded = 0
    tag_to_image = {}

    for item in ILLUSTRATIONS:
        dest_path = os.path.join(IMAGES_DIR, item["filename"])
        rel_path = f"images/{item['filename']}"
        url = item["url"]

        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        try:
            with urllib.request.urlopen(req) as resp:
                data = resp.read()

            # Verify JPEG header
            if not data.startswith(b"\xff\xd8\xff"):
                print(f"Warning: {item['filename']} does not have standard JPEG header!")

            with open(dest_path, "wb") as f:
                f.write(data)

            print(f"✓ Downloaded {item['filename']:<30} ({len(data):>7,} bytes) <- {url}")
            downloaded += 1

            if item["block_tag"]:
                tag_to_image[item["block_tag"]] = rel_path

        except Exception as e:
            print(f"✗ Failed {item['filename']} from {url}: {e}")

    print(f"\nSuccessfully downloaded {downloaded} / {len(ILLUSTRATIONS)} images.\n")

    # Link images in JSON files
    print("=== Linking Images to Dataset Blocks ===")

    for item in ILLUSTRATIONS:
        ch_id = item["chapter_id"]
        tag = item["block_tag"]
        if not ch_id or not tag:
            continue

        ch_path = os.path.join(JSON_DIR, f"{ch_id}.json")
        if not os.path.exists(ch_path):
            continue

        with open(ch_path, "r", encoding="utf-8") as f:
            blocks = json.load(f)

        changed = False
        for b in blocks:
            if b.get("tag") == tag:
                b["image"] = f"images/{item['filename']}"
                print(f"[{ch_id}.json] Linked block {b['id']} ({tag}) -> images/{item['filename']}")
                changed = True

        if changed:
            with open(ch_path, "w", encoding="utf-8") as f:
                json.dump(blocks, f, ensure_ascii=False, indent=2)
            print(f"Saved {os.path.basename(ch_path)} with linked image.")

    # Update Master JSON
    if os.path.exists(MASTER_PATH):
        with open(MASTER_PATH, "r", encoding="utf-8") as mf:
            master = json.load(mf)
        for ch in master.get("chapters", []):
            ch_id = ch["chapter_id"]
            ch_json_file = os.path.join(JSON_DIR, f"{ch_id}.json")
            if os.path.exists(ch_json_file):
                with open(ch_json_file, "r", encoding="utf-8") as cf:
                    ch["paragraphs"] = json.load(cf)
        with open(MASTER_PATH, "w", encoding="utf-8") as mf:
            json.dump(master, mf, ensure_ascii=False, indent=2)
        print("\nMaster JSON the_heroes_raw.json synchronized with image links.")

if __name__ == "__main__":
    download_and_link()
