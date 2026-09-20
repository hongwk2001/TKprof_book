"""
Rebuild the Korean retail sample to get its dead air under the QC gate.

check_audio_quality.py measured sample.mp3 and sample_retail_3min.mp3 at 15.5%
silence across the narration body (max 12%), with 41% of pauses landing in a
single 100 ms bucket -- the fixed-pause-constant signature described in
books/dracula/NARRATION_REJECTION_ANALYSIS.md.

Nothing Authors Republic checks automatically catches this: the sample's
length, padding, bitrate, peak and RMS are all in range. But the retail sample
is the track every prospective buyer auditions, so the dead air costs more here
than anywhere else in the book.

The fix compresses pauses rather than capping them. A hard cap would pile every
long gap onto the cap value and make the bucket statistic worse; scaling the
excess (new = cap + (old - cap) * SLOPE) shortens the long gaps while keeping
them distinguishable from each other.

Detection mirrors the gate exactly -- silencedetect=noise=-40dB:d=0.15 -- so
the measurement being optimised is the one that is checked. The cap walks down
until check_file() reports the ratio at or under TARGET_PCT, leaving margin
below the 12% limit.

The two source files are near-identical (115.17 s vs 115.28 s, same levels,
same 15.5% dead air). Only one is needed, and sample.mp3 is the name every
other book in this repo uses, so sample_retail_3min.mp3 is retired.

Usage:
    ../../venv/Scripts/python.exe fix_sample_ko.py
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..")))
from check_audio_quality import check_file  # noqa: E402

DIR = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(DIR, "final_audio_ko_ready")
SRC = os.path.join(PKG, "sample.mp3")
DUPE = os.path.join(PKG, "sample_retail_3min.mp3")

SR = 44100
BITRATE = "256k"
PAD_S = 2.0                 # matches the rest of the package
THRESH_DB = -40.0           # the gate's silencedetect threshold
MIN_PAUSE_S = 0.15          # the gate's silencedetect duration
SLOPE = 0.25                # how much of a pause's excess survives
TARGET_PCT = 10.5           # aim below the 12% limit, with margin


def decode(path):
    p = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", path, "-f", "f32le",
         "-ac", "1", "-ar", str(SR), "-"],
        capture_output=True)
    return np.frombuffer(p.stdout, dtype="<f4").copy()


def edges(x, thr_db=-60.0):
    """Sample indices of the first and last non-silent sample."""
    nz = np.nonzero(np.abs(x) > 10 ** (thr_db / 20))[0]
    return (nz[0], nz[-1] + 1) if len(nz) else (0, len(x))


def pause_runs(x):
    """Silence runs at the gate's threshold, as (start, stop) sample pairs."""
    quiet = np.abs(x) <= 10 ** (THRESH_DB / 20)
    if not quiet.any():
        return []
    edge = np.diff(quiet.astype(np.int8))
    starts = list(np.nonzero(edge == 1)[0] + 1)
    stops = list(np.nonzero(edge == -1)[0] + 1)
    if quiet[0]:
        starts.insert(0, 0)
    if quiet[-1]:
        stops.append(len(quiet))
    floor = int(MIN_PAUSE_S * SR)
    return [(a, b) for a, b in zip(starts, stops) if b - a >= floor]


def compress(body, cap_s, jitter=0.0, seed=20260920):
    """Shorten every pause past cap_s, keeping SLOPE of the excess.

    jitter spreads the compressed lengths by +/- that fraction. Without it the
    scaling maps a wide range of pauses onto a narrow one and they pile into a
    single 100 ms bucket -- on English chapter 5 the bucket statistic went from
    21% (passing) to 46% (flagged mechanical) before this was added. The RNG is
    seeded so a rebuild reproduces the same cuts.
    """
    cap = int(cap_s * SR)
    rng = np.random.default_rng(seed)
    out, prev = [], 0
    floor = int(MIN_PAUSE_S * SR)
    for a, b in pause_runs(body):
        n = b - a
        if n <= cap and not jitter:
            continue
        keep = n if n <= cap else cap + int((n - cap) * SLOPE)
        if jitter:
            # Jitter every gap, not just the compressed ones. Kokoro emits
            # fixed pause constants -- 26 of chapter 5's gaps sit at exactly
            # 0.2 s -- so leaving short pauses untouched leaves a pile in one
            # bucket however well the long ones are spread.
            keep = int(keep * rng.uniform(1.0 - jitter, 1.0 + jitter))
        keep = max(floor, min(keep, n))
        out.append(body[prev:a + keep])
        prev = b
    out.append(body[prev:])
    return np.concatenate(out) if out else body


def encode(samples, out_path, target_i):
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


def main():
    before = check_file(SRC)
    print(f"before  {before['duration']:.2f}s  rms {before['rms_db']:.2f}  "
          f"silence {before['silence_ratio_pct']:.1f}%  "
          f"top bucket {before['top_pause_bucket_pct']:.0f}%")

    x = decode(SRC)
    lo, hi = edges(x)
    body = x[lo:hi]

    for name, path in (("sample.mp3", SRC), ("sample_retail_3min.mp3", DUPE)):
        bak = path + ".deadair.bak"
        if os.path.exists(path) and not os.path.exists(bak):
            os.replace(path, bak)
            print(f"backed up {name} -> {os.path.basename(bak)}")

    for cap_s in (0.30, 0.26, 0.22, 0.18, 0.15):
        out = compress(body, cap_s)
        encode(out, SRC, target_i=-20.0)
        r = check_file(SRC)
        print(f"cap {cap_s:.2f}s -> {r['duration']:.2f}s  "
              f"rms {r['rms_db']:.2f}  peak {r['peak_db']:.2f}  "
              f"silence {r['silence_ratio_pct']:.1f}%  "
              f"top bucket {r['top_pause_bucket_pct']:.0f}%")
        if r["silence_ratio_pct"] <= TARGET_PCT:
            break

    r = check_file(SRC)
    print(f"\nafter   {r['status']}  lead {r['leading_silence']:.2f}s  "
          f"trail {r['trailing_silence']:.2f}s")
    for e in r.get("errors", []):
        print(f"  ERROR: {e}")
    for w in r.get("warnings", []):
        print(f"  warn:  {w}")
    print("\nsample_retail_3min.mp3 retired; sample.mp3 is the retail sample.")
    print("Originals kept as *.deadair.bak -- delete once you have listened.")


if __name__ == "__main__":
    main()
