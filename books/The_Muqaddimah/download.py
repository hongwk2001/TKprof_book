import urllib.request

base_url = "https://archive.org/download/1_20230830_20230830_1222/"
files = ['1_djvu.txt', '2_djvu.txt', '3_djvu.txt', '4_djvu.txt', '5_djvu.txt']

combined_text = ""

for f in files:
    url = base_url + f
    print(f"Downloading {f}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            combined_text += text + "\n\n"
    except Exception as e:
        print(f"Failed to download {f}: {e}")

with open("The_Muqaddimah_Original.txt", "w", encoding="utf-8") as out:
    out.write(combined_text)

print("Saved successfully to The_Muqaddimah_Original.txt")
