import os
import urllib.request
import urllib.parse

IMAGE_TITLES = {
    "cover.jpg": "Stories of beowulf viking ship cover.jpg",
    "illu_grendel.jpg": "Stories of beowulf grendel.jpg",
    "illu_water_witch.jpg": "Stories of Beowulf water witch trying to stab beowulf.jpg",
    "illu_grendel_head.jpg": "Stories of beowulf head of grendel.jpg",
    "illu_dragon.jpg": "Beowulf and the dragon.jpg",
    "illu_death.png": "Beowulf death.png"
}

IMAGES_DIR = r"D:\git_repo\TKprof_book\books\beowulf\images"
os.makedirs(IMAGES_DIR, exist_ok=True)

for filename, title in IMAGE_TITLES.items():
    dest_path = os.path.join(IMAGES_DIR, filename)
    url = "https://commons.wikimedia.org/wiki/Special:FilePath/" + urllib.parse.quote(title)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 TKPROF-Bot'})
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"Success: {dest_path}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        print(f"Failed to download {filename}: {e}")
