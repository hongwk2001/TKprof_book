import urllib.request
import os

music_url = "https://upload.wikimedia.org/wikipedia/commons/c/c5/Bach_-_Cello_Suite_No._1_in_G_Major_-_I._Prelude.ogg"
music_path = "d:/git_repo/TKprof_book/books/richest_man_in_babylon/background_music.ogg"

req = urllib.request.Request(music_url, headers={'User-Agent': 'Mozilla/5.0'})

print(f"Downloading {music_url}...")
try:
    with urllib.request.urlopen(req) as response, open(music_path, 'wb') as out_file:
        out_file.write(response.read())
    print("Music downloaded successfully.")
except Exception as e:
    print(f"Failed to download music: {e}")
