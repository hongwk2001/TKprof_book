import os
import re
import urllib.request

html_path = "original_gutenberg.html"
images_dir = "images"
base_url = "https://www.gutenberg.org/files/98/98-h/images/"

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

matches = set(re.findall(r'src="images/([^"]+\.jpg)"', html))
print(f"Found {len(matches)} images.")

for img in matches:
    url = base_url + img
    dest = os.path.join(images_dir, img)
    if not os.path.exists(dest):
        print(f"Downloading {img}...")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print(f"Failed to download {img}: {e}")
print("Done!")
