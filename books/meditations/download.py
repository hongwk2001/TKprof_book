import urllib.request
import os

BASE_DIR = r"d:\git_repo\TKprof_book\books\meditations"
os.makedirs(BASE_DIR, exist_ok=True)

CHRYSTAL_URL = "https://www.gutenberg.org/cache/epub/66978/pg66978.txt"
CHRYSTAL_FILE = os.path.join(BASE_DIR, "meditations_chrystal_raw.txt")

LONG_URL = "https://www.gutenberg.org/cache/epub/15877/pg15877.txt"
LONG_FILE = os.path.join(BASE_DIR, "meditations_long_raw.txt")

def download(url, filename):
    print(f"Downloading {url} to {filename}...")
    try:
        # Use a user-agent to prevent 403 Forbidden from Gutenberg
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        )
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print("Success.")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    download(CHRYSTAL_URL, CHRYSTAL_FILE)
    download(LONG_URL, LONG_FILE)
