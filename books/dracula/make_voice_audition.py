"""Audition Kokoro narrator voices on the same Dracula passage.

The current narrator (bm_fable) is graded C and trained on minutes of data,
which is why it reads blurry. Kokoro's own VOICES.md grades:

    af_heart  A     af_bella  A-    af_nicole B-    bf_emma  B-
    am_michael C+   am_puck   C+    am_fenrir C+    bm_fable C  (current)

Every British male voice is C or below, so a clearer narrator means changing
accent or gender. This renders each candidate so that is a listening decision,
not a spec-sheet one.

Usage:  venv/Scripts/python.exe books/dracula/make_voice_audition.py
Writes: books/dracula/voice_audition/<voice>.mp3
"""
import os
import subprocess

import numpy as np
import soundfile as sf

import make_english_audiobook as mk

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_audition")
os.makedirs(OUT, exist_ok=True)

# Every English voice. The upstream grades are the model author's own
# subjective ratings and did not survive listening -- af_nicole is graded B-
# and sounds like a sick person, while C-graded bm_fable was judged clearest.
# So audition the lot and decide by ear; Kokoro is fast enough that this costs
# minutes.
BANNED = {"af_nicole"}          # rejected on listening 2026-09-15

ALL_VOICES = [
    # US female
    "af_alloy", "af_aoede", "af_bella", "af_heart", "af_jessica", "af_kore",
    "af_nova", "af_river", "af_sarah", "af_sky",
    # US male
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa",
    # UK female
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    # UK male
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
]
CANDIDATES = [(v, {"a": "US", "b": "UK"}[v[0]] + " " +
               {"f": "female", "m": "male"}[v[1]])
              for v in ALL_VOICES if v not in BANNED]

# Real narration, with a heading first: headings are where the current build
# sounded worst, so they belong in the audition.
TEXT = ("Chapter 1. Jonathan Harker's Journal. "
        "The time of the year is come when the dead travel fast. "
        "I could see that the driver was making for the great archway, and "
        "beyond it the courtyard lay silent under the moon. What manner of "
        "place had I come to, and among what kind of people?")


def main():
    text = mk.normalize(TEXT)
    for voice, label in CANDIDATES:
        if os.path.exists(os.path.join(OUT, f"{voice}.mp3")):
            print(f"[skip] {voice:12} already rendered")
            continue
        try:
            y = mk.synth(text, voice)
        except Exception as e:
            print(f"[fail] {voice:12} {type(e).__name__}: {str(e)[:60]}")
            continue
        if y is None or y.size == 0:
            print(f"[fail] {voice:12} produced nothing")
            continue
        y = mk.trim(y)
        peak = float(np.max(np.abs(y)))
        if peak > 0:
            y = y * (0.95 / peak)
        wav = os.path.join(OUT, f"_{voice}.wav")
        mp3 = os.path.join(OUT, f"{voice}.mp3")
        sf.write(wav, y, mk.SR, subtype="PCM_16")
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", wav,
            "-af", "loudnorm=I=-20:TP=-3.5:LRA=7",
            "-ar", "44100", "-ac", "1", "-b:a", "192k", mp3,
        ], check=True)
        os.remove(wav)
        print(f"[ok] {voice:12} {label:32} {y.size/mk.SR:5.1f}s")


if __name__ == "__main__":
    main()
