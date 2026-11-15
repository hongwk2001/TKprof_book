"""
Align the Korean credits tracks with the cover art.

The cover uploaded to Authors Republic reads "낭독: TKPROF AI", but both credits
tracks say "선희 낭독" (Sunhi, the ko-KR-SunHiNeural voice name) and
metadata.md records no Korean narrator at all. AR requires the narrator credit
to match exactly across metadata, cover art and the opening/closing tracks, so
this is a rejection waiting independently of the two reasons already given.

The cover is already uploaded and correct, so the tracks move to match it.

Open question this cannot settle: how ko-KR-SunHiNeural pronounces "TKPROF AI"
written in Latin script. It may spell it out, mangle it, or read it cleanly.
So both spellings are rendered for a listening decision:

    latin   -> "TKPROF AI"        matches the cover glyph-for-glyph
    hangul  -> "티케이프로프 에이아이"  guaranteed pronunciation

Usage:  venv/Scripts/python.exe books/the_enchanted_april/fix_credits_ko.py
Writes: books/the_enchanted_april/credits_ko_test/
"""
import asyncio
import io
import os
import subprocess

import sys

import edge_tts

# Hangul in the console crashes Windows' default cp1252 encoding.
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(DIR, "credits_ko_test")
os.makedirs(OUT, exist_ok=True)

VOICE = "ko-KR-SunHiNeural"
BITRATE = "256k"
TITLE = "마법에 걸린 4월"
AUTHOR = "엘리자베스 폰 아르님"

NAMES = {
    "latin": "TKPROF AI",
    "hangul": "티케이프로프 에이아이",
}


def texts(narrator):
    # Opening must contain ONLY title, author, narrator.
    opening = f"{TITLE}.\n{AUTHOR} 지음.\n{narrator} 낭독."
    # Closing must be "The End" or the same info prefixed with "this has been".
    closing = (f"끝. 이것으로 {AUTHOR} 지음, {narrator} 낭독의 "
               f"{TITLE} 오디오북이 끝났습니다.")
    return opening, closing


async def synth(text, path):
    await edge_tts.Communicate(text, VOICE).save(path)


def master(raw, out, target_i):
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", raw,
        "-af", f"loudnorm=I={target_i}:TP=-3.5:LRA=7,"
               "adelay=1500|1500,apad=pad_dur=1.5",
        "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out,
    ], check=True)
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", out], capture_output=True, text=True).stdout)


def main():
    for tag, narrator in NAMES.items():
        opening, closing = texts(narrator)
        for kind, text in (("opening", opening), ("closing", closing)):
            raw = os.path.join(OUT, f"_{tag}_{kind}_raw.mp3")
            asyncio.run(synth(text, raw))
            out = os.path.join(OUT, f"{kind}_{tag}.mp3")
            # -19 LUFS: -16 put a short track at exactly -18.0 dB RMS, on AR's
            # upper limit with no margin.
            d = master(raw, out, "-19")
            os.remove(raw)
            print(f"[ok] {kind:8} {tag:7} {d:5.1f}s  \"{narrator}\"")


if __name__ == "__main__":
    main()
