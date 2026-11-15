"""
Regenerate the Korean closing track to Authors Republic's rules.

AR rejected this title 2026-07-17: "Closing track contains too much
information." The closing was generated from copyright_ko.txt, which is 1,865
bytes -- it opens with a compliant sentence and then continues into copyright
notes, edition background and acknowledgements. The result ran 116.6 seconds.

AR allows only:
    "The End"
  or
    "This has been {Title}. Written by {Author}. Narrated by {Narrator}."

copyright_ko.txt's FIRST sentence is already exactly that form, so the fix is
to keep it and drop everything after. AR's own guidance is to move the extra
content into a separate chapter track if it is wanted at all.

Mastering matches the rest of the Korean set: 256 kbps CBR, 44.1 kHz mono,
loudnorm, and 1-5 s of padding at each end. Loudness is targeted at -19 LUFS. -16 was tried first and landed the track at
exactly -18.0 dB RMS -- on AR's upper limit with no margin, the mirror image of
the problem that pushes over-padded short tracks to the -23 floor.
"""
import asyncio
import os
import subprocess
import sys

import edge_tts

DIR = os.path.dirname(os.path.abspath(__file__))
VOICE = "ko-KR-SunHiNeural"          # 선희, the narrator named in the text
BITRATE = "256k"                     # matches the rest of this title

# The compliant first sentence of copyright_ko.txt, verbatim:
# "The End. This concludes the audiobook of The Enchanted April, written by
#  Elizabeth von Arnim, narrated by Sunhi."
CLOSING = ("끝. 이것으로 엘리자베스 폰 아르님 지음, 선희 낭독의 "
           "마법에 걸린 4월 오디오북이 끝났습니다.")

TARGETS = [
    os.path.join(DIR, "final_audio_ko_ready", "closing.mp3"),
    os.path.join(DIR, "final_audio_ko", "closing.mp3"),
]


async def synth(path):
    await edge_tts.Communicate(CLOSING, VOICE).save(path)


def main():
    raw = os.path.join(DIR, "_closing_raw.mp3")
    asyncio.run(synth(raw))

    for out in TARGETS:
        if not os.path.isdir(os.path.dirname(out)):
            print(f"[skip] {out} (folder missing)")
            continue
        bak = out + ".toolong.bak"
        if os.path.exists(out) and not os.path.exists(bak):
            before = float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
            os.replace(out, bak)
        elif os.path.exists(out):
            before = float(subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
            os.remove(out)          # backup already taken on an earlier run
        else:
            before = 0.0
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-i", raw,
            "-af", "loudnorm=I=-19:TP=-3.5:LRA=7,"
                   "adelay=1500|1500,apad=pad_dur=1.5",
            "-ar", "44100", "-ac", "1", "-b:a", BITRATE, out,
        ], check=True)
        after = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", out], capture_output=True, text=True).stdout)
        print(f"[ok] {os.path.relpath(out, DIR)}  {before:.1f}s -> {after:.1f}s")

    os.remove(raw)
    print("\nOld tracks kept as *.toolong.bak -- delete once verified.")


if __name__ == "__main__":
    main()
