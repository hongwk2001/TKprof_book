"""Compare candidate voices on SEWARD's text -- 41% of the book.

The earlier narrator comparison was useless: chapter 1's opening is 99.3%
Jonathan Harker, so swapping the narrator voice changed two words out of a
103-second file and every candidate sounded identical.

Seward is the right test. He carries 378,125 characters, 41.1% of the runtime,
more than Harker and Mina combined. Whatever voice reads him is the voice the
audiobook mostly IS.
"""
import os
import sys

import make_english_audiobook as mk
import make_english_audiobook_v2 as v2

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "seward_compare")
os.makedirs(OUT, exist_ok=True)

# Real Seward, from chapter 5.
TEXT = (
    "Dr Seward's Diary. May 25. My appetite is at its lowest ebb today. "
    "I cannot eat and I cannot rest, so I am turning to my diary instead. "
    "Ever since I was rejected yesterday, I have been left with a terrible "
    "sense of emptiness; nothing in the world feels important enough to be "
    "worth doing. Knowing that the only cure for this sort of melancholy is "
    "work, I went down to the wards among the patients. I singled out one "
    "who has provided me with a highly fascinating psychological study. "
    "His mania is so strong, and so unlike anything I have met before, that "
    "I am determined to understand it as fully as I can. Today I seem to be "
    "nearer than ever to reaching the heart of his secret."
)

CANDIDATES = [
    ("af_heart", "US female"),
    ("af_bella", "US female"),
    ("bf_emma", "UK female"),
    ("bm_fable", "UK male"),
    ("bm_lewis", "UK male -- CURRENT Seward, the rejected build"),
]


def main():
    text = mk.normalize(TEXT)
    for voice, label in CANDIDATES:
        y = mk.synth(text, voice)
        if y is None or y.size == 0:
            print(f"[fail] {voice}")
            continue
        clip = v2.squeeze(mk.trim(y, thresh_db=v2.TRIM_DB,
                                  keep_ms=v2.TRIM_KEEP_MS))
        secs = v2.master([clip], os.path.join(OUT, f"{voice}.mp3"))
        print(f"[ok] {voice:10} {label:44} {secs:5.1f}s")


if __name__ == "__main__":
    main()
