"""
Quick remix script - reuses existing cached TTS clips, only redoes the music mixing.
Skips all edge-tts generation entirely.
"""
import os
import glob
import json
from pydub import AudioSegment

SCRIPTS_DIR = "scripts"
TEMP_DIR = "temp_audio"
OUTPUT_DIR = "final_audio"

def remix_chapter(ch_num):
    script_file = os.path.join(SCRIPTS_DIR, f"script_ch_{ch_num}.json")
    if not os.path.exists(script_file):
        print(f"Script not found: {script_file}")
        return

    with open(script_file, 'r', encoding='utf-8') as f:
        script = json.load(f)

    print(f"Remixing Chapter {ch_num} using cached clips...")

    # 1. Load all existing cached clips in order
    audio_segments = []
    for i, segment in enumerate(script):
        if not segment['text'].strip():
            continue
        temp_mp3 = os.path.join(TEMP_DIR, f"ch{ch_num}_{i:03d}.mp3")
        if os.path.exists(temp_mp3):
            clip = AudioSegment.from_mp3(temp_mp3)
            audio_segments.append(clip)
        else:
            print(f"  Warning: missing clip {temp_mp3}, skipping.")

    print(f"  Loaded {len(audio_segments)} cached clips.")

    # 2. Combine with pause
    combined = AudioSegment.empty()
    short_silence = AudioSegment.silent(duration=300)
    for clip in audio_segments:
        combined += clip + short_silence

    # 3. Add cinematic intro + chime (no Bach bumper)
    print("  Applying cinematic intro and chime...")
    cinematic = AudioSegment.from_mp3("freesound_community-cinematic-intro-6097.mp3")
    chime = AudioSegment.from_mp3("chime.mp3")

    final_audio = (
        cinematic                          # Cinematic intro at very beginning
        + AudioSegment.silent(duration=500)
        + chime                            # Bell chime before narration
        + AudioSegment.silent(duration=500)
        + combined                         # Main narration
        + AudioSegment.silent(duration=500)
        + chime                            # Bell chime after narration
    )

    out_file = os.path.join(OUTPUT_DIR, f"final_ch_{ch_num}.mp3")
    final_audio.export(out_file, format="mp3")
    print(f"  Done! Saved to {out_file}")

if __name__ == "__main__":
    import sys
    ch = sys.argv[1] if len(sys.argv) > 1 else "06"
    remix_chapter(ch)
