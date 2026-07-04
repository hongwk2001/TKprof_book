import os
import glob
import subprocess
import math

BASE_DIR = "books/science_of_getting_rich"
CHAPTERS_DIR = os.path.join(BASE_DIR, "chapters")
AUDIO_DIR = os.path.join(BASE_DIR, "final_audio")

def count_words(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    return len(content.split())

# 1. Original Word Count
raw_files = glob.glob(os.path.join(CHAPTERS_DIR, "raw_ch_*.txt"))
original_words = sum(count_words(f) for f in raw_files)

# 2. New Word Count
new_files = glob.glob(os.path.join(CHAPTERS_DIR, "ch_*_en.txt"))
new_words = sum(count_words(f) for f in new_files)

# 3. Audio duration (Reading Time)
audio_files = glob.glob(os.path.join(AUDIO_DIR, "*.mp3"))
total_duration_sec = 0.0

for f in audio_files:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", f
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        total_duration_sec += float(output)
    except Exception as e:
        print(f"Error checking {f}: {e}")

total_hours = math.floor(total_duration_sec / 3600)
total_minutes = math.floor((total_duration_sec % 3600) / 60)
total_seconds = math.floor(total_duration_sec % 60)

print(f"Original Word Count: {original_words:,} words")
print(f"New Modernized Word Count: {new_words:,} words")
print(f"Total Reading Time (Audio Duration): {total_hours}h {total_minutes}m {total_seconds}s")
