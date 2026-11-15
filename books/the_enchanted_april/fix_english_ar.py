"""
Rebuild the English Authors Republic package from the unsplit masters.

final_audio_ready/ cannot be repaired in place. Three defects are baked into
its files:

  * 14 chapters were split without re-padding the parts, so part1 has 2.000 s
    of lead and 0.000 s of tail and part2 the reverse (ch 02, 04, 07, 09, 12,
    13, 14, 15, 16, 17, 18, 19, 20, 23). This also fails the audit's noise
    floor test, which samples 0.2-0.8 s in and lands on narration.
  * closing.mp3 and final_track_24_appendix.mp3 are 2.000 s of pure digital
    silence -- empty files, with no backup. The closing was destroyed by an
    attempt to fix AR's 2026-07-17 rejection ("Closing track contains too much
    information"): the trim consumed the whole file and fix_audio_quality.py
    padded the empty result to 1000 ms + 1000 ms.
  * 39 of 42 tracks exceed the 12% dead-air limit -- chapter 5 measures 17.8%
    with 17 pauses piled at exactly 1.3 s.

So this reads final_audio/ instead and writes a new final_audio_en_ar/,
leaving final_audio_ready/ intact until the rebuild is verified.

Pause compression is the technique proven on the Korean retail sample
(fix_sample_ko.py): 15.5% -> 9.7%. It scales each pause's excess rather than
capping it, so long gaps shorten without piling onto one value, and it only
ever cuts inside runs already below -40 dBFS for >= 0.15 s -- no speech can be
removed.

Chapters over MAX_PART_S are split at the longest pause near each boundary, so
a cut never lands mid-sentence, and every part is padded independently.

Credits tracks are rendered from introduction_en.txt and CLOSING below.
CLOSING uses Authors Republic's own example script verbatim. Do not reuse
copyright_en.txt's first line: it reads "The End. This concludes the audiobook
of ...", and AR's 2026-07-17 letter allows only "The End" or the opening's
information prefixed with "This has been" or "You have been listening to".
"This concludes" is neither.

Usage:
    ../../venv/Scripts/python.exe fix_english_ar.py 5          # one chapter
    ../../venv/Scripts/python.exe fix_english_ar.py credits    # opening+closing
    ../../venv/Scripts/python.exe fix_english_ar.py all        # everything
"""
import math
import os
import re
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from check_audio_quality import check_file            # noqa: E402
from fix_sample_ko import decode, edges, compress     # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(DIR, "final_audio")
DST = os.path.join(DIR, "final_audio_en_ar")

SR = 44100
BITRATE = "256k"
PAD_S = 2.0
MAX_PART_S = 960.0            # 16 min; AR's own limit is far higher, but the
                              # Korean package splits at this size and the
                              # parts upload without timing out
TARGET_I = -19.5              # lands RMS near -19.4, mid-range of -23..-18
CAPS = (0.30, 0.26, 0.22, 0.18, 0.15)
TARGET_PCT = 10.5
JITTER = 0.50              # spread compressed pauses across buckets; 0.35 left the
                           # bucket statistic at 38%, over the 30% threshold

CLOSING = ("This has been The Enchanted April. "
           "Written by Elizabeth von Arnim. Narrated by TKPROF AI.")


def encode(samples, out_path, target_i=TARGET_I):
    raw = out_path + ".raw"
    samples.astype("<f4").tofile(raw)
    pad = f"adelay={int(PAD_S * 1000)},apad=pad_dur={PAD_S}"
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ac", "1",
         "-ar", str(SR), "-i", raw,
         "-af", f"loudnorm=I={target_i}:TP=-3.5:LRA=11,{pad}",
         "-ar", str(SR), "-ac", "1", "-b:a", BITRATE, out_path],
        check=True)
    os.remove(raw)


def split_points(body, n):
    """Cut indices for n parts, each nudged to the longest nearby pause.

    A cut placed on raw arithmetic lands mid-word. Searching a +/-15 s window
    around each target for the quietest stretch puts it in a breath instead.
    """
    if n <= 1:
        return []
    quiet = np.abs(body) <= 10 ** (-40.0 / 20)
    win = int(15.0 * SR)
    cuts = []
    for i in range(1, n):
        target = int(len(body) * i / n)
        lo, hi = max(0, target - win), min(len(body), target + win)
        seg = quiet[lo:hi]
        if not seg.any():
            cuts.append(target)
            continue
        # longest run of quiet in the window, cut at its middle
        best_len = best_mid = 0
        run = 0
        for j, q in enumerate(seg):
            run = run + 1 if q else 0
            if run > best_len:
                best_len, best_mid = run, j - run // 2
        cuts.append(lo + best_mid if best_len else target)
    return cuts


def process_chapter(name):
    path = os.path.join(SRC, name)
    stem = name[:-4]
    before = check_file(path)
    x = decode(path)
    lo, hi = edges(x)
    body = x[lo:hi]

    for cap in CAPS:
        out = compress(body, cap, jitter=JITTER)
        tmp = os.path.join(DST, f"_{stem}.probe.mp3")
        encode(out, tmp)
        r = check_file(tmp)
        os.remove(tmp)
        if r["silence_ratio_pct"] is None or r["silence_ratio_pct"] <= TARGET_PCT:
            break

    n = max(1, math.ceil((len(out) / SR) / MAX_PART_S))
    cuts = [0] + split_points(out, n) + [len(out)]
    written = []
    for i in range(n):
        seg = out[cuts[i]:cuts[i + 1]]
        suffix = f"_part{i + 1}" if n > 1 else ""
        dest = os.path.join(DST, f"{stem}{suffix}.mp3")
        encode(seg, dest)
        written.append(dest)

    sil_before = before["silence_ratio_pct"]
    print(f"{name}  {before['duration']:7.1f}s -> "
          f"{sum(check_file(w)['duration'] for w in written):7.1f}s in {n} part(s)"
          f"   dead air {sil_before:.1f}% -> ", end="")
    for w in written:
        r = check_file(w)
        print(f"{r['silence_ratio_pct']:.1f}% " if r["silence_ratio_pct"]
              else "n/a ", end="")
    print()
    for w in written:
        r = check_file(w)
        flag = "PASS" if r["status"] == "PASS" else "FAIL"
        print(f"   {os.path.basename(w):34} {flag}  "
              f"{r['duration']:7.1f}s  rms {r['rms_db']:6.2f}  "
              f"peak {r['peak_db']:6.2f}  "
              f"lead {r['leading_silence']:.2f}  trail {r['trailing_silence']:.2f}")
        for e in r.get("errors", []):
            print(f"      ERROR: {e}")
    return written


def render_credits():
    """Render opening and closing with the lead Kokoro voice, af_heart.

    "TKPROF AI" in Latin script may be spelled out, mangled or read cleanly --
    the same open question fix_credits_ko.py raised for Korean and never
    settled. Both spellings are rendered for a listening decision.
    """
    from kokoro import KPipeline
    import soundfile as sf

    pipe = KPipeline(lang_code="a")
    opening = open(os.path.join(DIR, "introduction_en.txt"),
                   encoding="utf-8").read().strip()
    variants = {
        "latin": lambda s: s,
        "spelled": lambda s: s.replace("TKPROF AI", "T K PROF, A I"),
    }
    os.makedirs(os.path.join(DIR, "credits_en_test"), exist_ok=True)
    for label, fn in variants.items():
        for kind, text in (("opening", opening), ("closing", CLOSING)):
            wav = np.concatenate([a for _, _, a in
                                  pipe(fn(text), voice="af_heart", speed=1.0)])
            raw = os.path.join(DIR, "credits_en_test", f"{kind}_{label}.wav")
            sf.write(raw, wav, 24000)
            dest = os.path.join(DIR, "credits_en_test", f"{kind}_{label}.mp3")
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", raw, "-af",
                 f"loudnorm=I=-19:TP=-3.5:LRA=7,"
                 f"adelay={int(PAD_S * 1000)},apad=pad_dur={PAD_S}",
                 "-ar", str(SR), "-ac", "1", "-b:a", BITRATE, dest],
                check=True)
            os.remove(raw)
            r = check_file(dest)
            print(f"  {kind}_{label}.mp3  {r['status']}  {r['duration']:.2f}s  "
                  f"rms {r['rms_db']:.2f}  peak {r['peak_db']:.2f}")
    print("\nListen to credits_en_test/ and tell me which spelling to keep.")


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(DST, exist_ok=True)

    if arg == "credits":
        render_credits()
        return 0

    masters = sorted(f for f in os.listdir(SRC)
                     if re.match(r"final_track_\d+\.mp3$", f))
    if arg == "all":
        targets = masters
    elif arg.isdigit():
        targets = [f for f in masters if int(re.search(r"\d+", f).group()) == int(arg)]
    else:
        print(__doc__.strip().split("Usage:")[-1])
        print(f"\nmasters available: {len(masters)}")
        return 1

    if not targets:
        print(f"no master matching '{arg}'")
        return 1
    for name in targets:
        process_chapter(name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
