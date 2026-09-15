"""A/B a clarity EQ chain on a chosen Kokoro voice.

"Blurry" in a 24 kHz TTS source is usually two things: a build-up of low-mid
energy around 200-400 Hz that masks consonants, and weak presence in the
2-5 kHz band where intelligibility lives. Neither is fixable by swapping
voices, and both respond to EQ -- so this is worth trying before accepting a
voice that is merely the least bad.

There is no bandwidth above ~12 kHz to recover (the source is 24 kHz), so this
does not attempt any high-shelf "air" lift, which would only amplify hiss.

Usage:  venv/Scripts/python.exe books/dracula/make_clarity_test.py [voice]
"""
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(DIR, "voice_audition")
OUT = os.path.join(DIR, "clarity_test")
os.makedirs(OUT, exist_ok=True)

VOICE = sys.argv[1] if len(sys.argv) > 1 else "bm_fable"
SRC = os.path.join(SRC_DIR, f"{VOICE}.mp3")

CHAINS = {
    "A_raw": None,
    # gentle: clear the mud, modest presence lift
    "B_gentle": ("highpass=f=75,"
                 "equalizer=f=250:width_type=q:w=1.2:g=-2.5,"
                 "equalizer=f=3000:width_type=q:w=1.0:g=+2.5"),
    # stronger: more cut, more presence, slight compression for consistency
    "C_strong": ("highpass=f=80,"
                 "equalizer=f=300:width_type=q:w=1.2:g=-4,"
                 "equalizer=f=2200:width_type=q:w=1.2:g=+2,"
                 "equalizer=f=4500:width_type=q:w=1.4:g=+3,"
                 "acompressor=threshold=-18dB:ratio=2:attack=5:release=120"),
}


def main():
    if not os.path.exists(SRC):
        print(f"missing {SRC} -- run make_voice_audition.py first")
        return
    for name, chain in CHAINS.items():
        af = "loudnorm=I=-20:TP=-3.5:LRA=7"
        if chain:
            af = chain + "," + af
        out = os.path.join(OUT, f"{VOICE}_{name}.mp3")
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", SRC, "-af", af,
            "-ar", "44100", "-ac", "1", "-b:a", "192k", out,
        ], check=True)
        print(f"[ok] {os.path.basename(out)}")


if __name__ == "__main__":
    main()
