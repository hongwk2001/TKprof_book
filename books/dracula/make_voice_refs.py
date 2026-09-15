"""
Generate speaker-reference clips for Zonos voice cloning.

Zonos pins a voice with make_speaker_embedding(reference_audio), so each of the
seven cast voices needs one clean 10-15s sample. Rather than re-cast the book
from scratch, these are rendered with the same Kokoro voices already chosen in
make_english_audiobook.py: the casting decisions carry over unchanged, and
Zonos supplies what Kokoro could not -- prosody variation and 44.1 kHz.

Timbre is cloned from a 24 kHz source, but the OUTPUT is generated at Zonos'
own 44.1 kHz by its decoder, so the delivered bandwidth does not inherit
Kokoro's ceiling. Verify that with check_audio_quality.py rather than assuming.

Usage:  venv/Scripts/python.exe books/dracula/make_voice_refs.py
Writes: books/dracula/voice_refs/<kokoro_voice>.wav  (24 kHz mono PCM)
"""
import os
import sys

import numpy as np
import soundfile as sf

import make_english_audiobook as mk

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_refs")
os.makedirs(OUT, exist_ok=True)

# ~12s of in-character text per voice. Long enough for a stable embedding,
# varied enough in punctuation that the clone hears question and exclamation
# contours, not just flat declaratives.
REFS = {
    "bm_fable": (
        "The time of the year is come when the dead travel fast. "
        "I could see that the driver was making for the great archway, "
        "and beyond it the courtyard lay silent under the moon. "
        "What manner of place had I come to, and among what kind of people?"
    ),
    "bm_george": (
        "3 May. Bistritsa. Left Munich at 8:35 in the evening, on the first of "
        "May, arriving at Vienna early next morning. I had a hurried breakfast, "
        "and then set out to see the town. Is this a dream? I cannot tell. "
        "I must keep my wits about me, or I am lost."
    ),
    "bf_emma": (
        "I must keep writing at every chance, for I cannot tell when I shall "
        "see him again. Is he well? Is he safe? I have written out the whole "
        "of the journal, and I shall not rest until I understand it. "
        "Oh, my dear, what shall we do?"
    ),
    "bf_alice": (
        "Oh, I am so happy! Why are men so noble, and women so little worthy "
        "of them? Three proposals in one day! Is it not wonderful? "
        "I do not know what I have done to deserve such friends. "
        "And yet I am so tired, and I cannot think why."
    ),
    "bm_lewis": (
        "Let me record this exactly as it happened. The patient is more "
        "excitable than usual, and his talk of life has taken a new turn. "
        "I have never seen anything like it in all my practice. "
        "What does it mean? I must observe him closely tonight."
    ),
    "am_fenrir": (
        "There are mysteries which men can only guess at, which age by age "
        "they solve only in part! Do you not see, my friend? "
        "You are a clever man, but you think too narrowly. "
        "Believe me, there are things done today that would have been thought "
        "madness a hundred years ago."
    ),
    "bm_daniel": (
        "I have come at once, as you asked. Tell me plainly what is wrong, "
        "and I shall do whatever is needed. Is she worse? "
        "I would give my life for hers, and gladly. "
        "There is nothing I would not do, if only you will tell me how."
    ),
}


def main():
    for voice, text in REFS.items():
        y = mk.synth(mk.normalize(text), voice)
        if y is None or y.size == 0:
            print(f"[fail] {voice}")
            continue
        y = mk.trim(y)
        peak = float(np.max(np.abs(y)))
        if peak > 0:
            y = y * (0.95 / peak)          # normalize; embeddings prefer clean level
        path = os.path.join(OUT, f"{voice}.wav")
        sf.write(path, y, mk.SR, subtype="PCM_16")
        print(f"[ok] {voice:<12} {y.size / mk.SR:5.1f}s -> {path}")


if __name__ == "__main__":
    main()
