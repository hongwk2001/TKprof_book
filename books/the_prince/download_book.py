import urllib.request
import os

url = "https://www.gutenberg.org/cache/epub/1232/pg1232.txt"
out_path = r"d:\git_repo\TKprof_book\books\the_prince\the_prince_raw.txt"

print(f"Downloading {url}...")
try:
    urllib.request.urlretrieve(url, out_path)
    print(f"Successfully downloaded to {out_path}")
except Exception as e:
    print(f"Error downloading: {e}")
