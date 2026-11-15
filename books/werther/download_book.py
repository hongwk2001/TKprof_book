import os
import urllib.request

# Project Gutenberg #2527 - "The Sorrows of Young Werther"
# Johann Wolfgang von Goethe, trans. R. D. Boylan, ed. Nathen Haskell Dole
URL = "https://www.gutenberg.org/cache/epub/2527/pg2527.txt"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_OUT = os.path.join(BASE_DIR, "werther_raw.txt")

def download_source():
    print(f"Downloading from {URL}...")
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req) as response:
        content = response.read().decode("utf-8")

    with open(RAW_OUT, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully saved to {RAW_OUT} ({len(content)} characters, {len(content.splitlines())} lines)")

if __name__ == "__main__":
    download_source()
