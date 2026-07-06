from pydub import AudioSegment
import os

AUDIO_DIR = "books/beowulf/final_audio"
files = sorted(os.listdir(AUDIO_DIR))

total_duration_s = 0
issues = []

print(f"{'File':<35} {'Hz':>6} {'Ch':>3} {'kbps':>6} {'Duration':>10}")
print("-" * 65)

for fname in files:
    if not fname.endswith(".mp3"):
        continue
    fpath = os.path.join(AUDIO_DIR, fname)
    a = AudioSegment.from_mp3(fpath)
    size_mb = os.path.getsize(fpath) / (1024 * 1024)
    duration_s = len(a) / 1000
    bitrate_kbps = (size_mb * 8 * 1024) / duration_s
    total_duration_s += duration_s

    flag = ""
    if a.frame_rate < 44100 or bitrate_kbps < 192:
        flag = " ❌"
        issues.append(fname)

    mins = int(duration_s // 60)
    secs = int(duration_s % 60)
    print(f"{fname:<35} {a.frame_rate:>6} {a.channels:>3} {bitrate_kbps:>6.0f} {mins:>4}m{secs:02d}s{flag}")

total_mins = int(total_duration_s // 60)
total_secs = int(total_duration_s % 60)
print("-" * 65)
print(f"Total tracks: {len(files)}")
print(f"Total duration: {total_mins}m {total_secs}s ({total_duration_s/3600:.2f} hours)")
if issues:
    print(f"\n❌ Non-compliant tracks: {issues}")
else:
    print("\n✅ All tracks ACX compliant (44.1kHz, 192kbps+)")
