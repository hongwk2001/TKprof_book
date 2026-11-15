"""
fix_scaramouche_samples.py

Regenerates sample_ko.mp3 for Books 1, 2, 3.

Root cause of AR rejection:
  The source final_track_01_ko.mp3 has room-noise "silence" at the start.
  After gain normalization that quiet noise gets amplified above AR's strict
  silence threshold, so AR's detector sees it as audio content, not silence.

Fix strategy:
  1. Skip first 5s of source to bypass any existing leading content
  2. Clip 3 minutes of clean speech from that point
  3. Normalize the speech content ONLY
  4. Add clean digital silence pads AFTER normalization (so they stay at -inf dB)
"""

import os
import sys
import math
import subprocess

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from pydub import AudioSegment

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

BOOK_DIRS = {
    1: os.path.join(SCRIPT_DIR, "final_audio_book1"),
    2: os.path.join(SCRIPT_DIR, "final_audio_book2"),
    3: os.path.join(SCRIPT_DIR, "final_audio_book3"),
}

SAMPLE_RATE   = 44100
CHANNELS      = 2
BITRATE       = "256k"
LEAD_SILENCE  = 2000   # 2s leading  (clean digital zero)
TRAIL_SILENCE = 2000   # 2s trailing (clean digital zero)
SKIP_MS       = 5000   # skip first 5s of source to avoid room-noise intro
CLIP_MS       = 3 * 60 * 1000   # 3 minutes of content
TARGET_RMS_DB = -19.0


def normalize_to_rms(seg: AudioSegment, target_db: float) -> AudioSegment:
    if seg.dBFS == float("-inf"):
        return seg
    return seg.apply_gain(target_db - seg.dBFS)


def build_sample(src_path: str, out_path: str) -> bool:
    if not os.path.exists(src_path):
        print(f"  ✗ Source not found: {src_path}")
        return False

    print(f"  Loading: {os.path.basename(src_path)}")
    audio = AudioSegment.from_file(src_path, format="mp3")

    # Skip first 5s to skip any leading room-noise/silence from source
    content = audio[SKIP_MS:]
    # Clip 3 minutes of clean speech
    clip = content[:CLIP_MS]
    clip = clip.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)

    # Normalize SPEECH ONLY to target RMS
    clip = normalize_to_rms(clip, TARGET_RMS_DB)
    # Safety peak clamp
    if clip.max_dBFS > -3.0:
        clip = clip.apply_gain(-(clip.max_dBFS - (-3.1)))

    # Add CLEAN digital silence AFTER normalization
    silence_lead  = AudioSegment.silent(duration=LEAD_SILENCE,  frame_rate=SAMPLE_RATE).set_channels(CHANNELS)
    silence_trail = AudioSegment.silent(duration=TRAIL_SILENCE, frame_rate=SAMPLE_RATE).set_channels(CHANNELS)
    final = silence_lead + clip + silence_trail

    final.export(out_path, format="mp3", bitrate=BITRATE,
                 parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {os.path.basename(out_path)}")
    return True


def run_qc(fpath: str) -> bool:
    result = subprocess.run(
        [sys.executable, CHECK_SCRIPT, fpath],
        capture_output=True, text=True, encoding="utf-8"
    )
    output = result.stdout + result.stderr
    print(f"\n  [{os.path.basename(fpath)}]")
    for line in output.splitlines():
        if any(kw in line for kw in ["Status:", "Levels:", "Silence:", "Errors:", "  - "]):
            print(f"    {line.strip()}")
    return "Status: [FAIL]" not in output


def main():
    print("=" * 60)
    print("  Scaramouche KO Sample Fix (clean silence pads)")
    print("=" * 60)

    generated = []
    all_passed = True

    for book_num in [1, 2, 3]:
        src = os.path.join(BOOK_DIRS[book_num], "final_track_01_ko.mp3")
        out = os.path.join(BOOK_DIRS[book_num], "sample_ko.mp3")
        print(f"\n[Book {book_num} | KO | SAMPLE]")
        if build_sample(src, out):
            generated.append(out)

    print(f"\n\n{'='*60}")
    print("  QC AUDIT — Regenerated Samples")
    print(f"{'='*60}")

    for fpath in generated:
        if not run_qc(fpath):
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("  ✅ ALL SAMPLES PASSED QC")
    else:
        print("  ❌ SOME FAILED — see above")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
