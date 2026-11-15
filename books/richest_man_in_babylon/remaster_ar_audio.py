"""
remaster_ar_v2.py  -  Authors Republic Remaster (v2)
=====================================================
Fixes two issues flagged by Authors Republic on 2026-08-17:
  1. Track RMS too low (measured -23.9 to -25.1 dB by AR; must be -23 to -18 dB)
  2. No start-of-track silence detected

Root cause: The ORIGINAL final_audio/ files (not the ar_ready ones) were uploaded.
The originals have no leading silence and peak above -3 dB.

This script re-reprocesses final_audio/ -> final_audio_ar_ready/ with:
  - Two-pass FFmpeg loudnorm targeting I=-19 LUFS / TP=-3.0 / LRA=11
  - Exactly 3.0s of true digital silence prepended and appended
  - 256kbps CBR, 44100Hz, stereo

Usage:
  cd books/richest_man_in_babylon
  python remaster_ar_v2.py
"""

import os
import sys
import json
import subprocess
import tempfile
import re

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
SRC_DIR     = os.path.join(SCRIPT_DIR, "raw_audio")
DST_DIR     = os.path.join(SCRIPT_DIR, "final_audio_ar_ready")

TARGET_I    = -20.0   # Integrated LUFS target
TARGET_TP   = -3.0    # True peak dB
TARGET_LRA  = 11.0    # Loudness range
SILENCE_S   = 3.0     # Seconds of silence at start and end
BITRATE     = "256k"
SAMPLE_RATE = "44100"
CHANNELS    = "2"


def two_pass_loudnorm(src, norm_out):
    """Two-pass loudnorm: measure then apply in linear mode."""
    # Pass 1: measure
    p1_filter = (
        "loudnorm=I={I}:LRA={LRA}:TP={TP}:print_format=json".format(
            I=TARGET_I, LRA=TARGET_LRA, TP=TARGET_TP
        )
    )
    r1 = subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-af", p1_filter, "-f", "null", "-"],
        capture_output=True, text=True
    )
    stderr = r1.stderr
    start = stderr.rfind("{")
    end   = stderr.rfind("}") + 1
    if start < 0 or end <= start:
        print("  ERROR: Pass-1 loudnorm JSON not found", file=sys.stderr)
        return False
    measured = json.loads(stderr[start:end])
    il   = measured["input_i"]
    itp  = measured["input_tp"]
    ilra = measured["input_lra"]
    ith  = measured["input_thresh"]
    off  = measured["target_offset"]

    # Pass 2: apply in linear mode
    p2_filter = (
        "loudnorm=I={I}:LRA={LRA}:TP={TP}"
        ":measured_I={il}:measured_LRA={ilra}:measured_TP={itp}"
        ":measured_thresh={ith}:offset={off}:linear=true"
    ).format(
        I=TARGET_I, LRA=TARGET_LRA, TP=TARGET_TP,
        il=il, ilra=ilra, itp=itp, ith=ith, off=off
    )
    r2 = subprocess.run(
        ["ffmpeg", "-y", "-i", src,
         "-af", p2_filter,
         "-ar", SAMPLE_RATE, "-ac", CHANNELS,
         "-b:a", BITRATE, "-c:a", "libmp3lame",
         norm_out],
        capture_output=True, text=True
    )
    if r2.returncode != 0:
        print("  ERROR pass-2: " + r2.stderr[-300:], file=sys.stderr)
        return False
    return True


def add_silence_pads(norm_path, silence_path, dst):
    """Concat: 3s silence + normalized content + 3s silence using file concat."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, dir=os.path.dirname(dst)) as fh:
        list_path = fh.name
        fh.write("file '" + silence_path.replace("\\", "/") + "'\n")
        fh.write("file '" + norm_path.replace("\\", "/") + "'\n")
        fh.write("file '" + silence_path.replace("\\", "/") + "'\n")
    try:
        r = subprocess.run(
            ["ffmpeg", "-y",
             "-f", "concat", "-safe", "0", "-i", list_path,
             "-c", "copy", dst],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            print("  ERROR concat: " + r.stderr[-300:], file=sys.stderr)
            return False
        return True
    finally:
        os.remove(list_path)


def verify_file(path):
    """Quick volumedetect + silencedetect check."""
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", path,
         "-filter_complex", "volumedetect;[0:a]silencedetect=noise=-70dB:d=0.5",
         "-f", "null", "-"],
        capture_output=True, text=True
    )
    rms_m  = re.search(r"mean_volume:\s+([-\d.]+)\s+dB", r.stderr)
    peak_m = re.search(r"max_volume:\s+([-\d.]+)\s+dB", r.stderr)
    starts = re.findall(r"silence_start:\s+([\d.]+)", r.stderr)
    ends   = re.findall(r"silence_end:\s+([\d.]+)", r.stderr)

    r2 = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True
    )
    dur = float(json.loads(r2.stdout)["format"]["duration"])

    leading  = float(ends[0]) if ends and starts and float(starts[0]) < 0.1 else 0.0
    trailing = (dur - float(starts[-1])) if starts and (dur - float(starts[-1])) > 0.4 else 0.0

    return {
        "rms":      float(rms_m.group(1))  if rms_m  else None,
        "peak":     float(peak_m.group(1)) if peak_m else None,
        "leading":  leading,
        "trailing": trailing,
        "dur":      dur,
    }


def main():
    os.makedirs(DST_DIR, exist_ok=True)
    mp3s = sorted(f for f in os.listdir(SRC_DIR) if f.lower().endswith(".mp3"))

    if not mp3s:
        print("No MP3 files found in " + SRC_DIR)
        sys.exit(1)

    print("Remastering " + str(len(mp3s)) + " files")
    print("  Source : " + SRC_DIR)
    print("  Output : " + DST_DIR)
    print("  Target : " + str(TARGET_I) + " LUFS / TP " + str(TARGET_TP) + " dB / " + str(SILENCE_S) + "s silence pads")
    print("=" * 70)

    ok = 0
    fail = 0

    with tempfile.TemporaryDirectory() as tmp:
        # Build silence pad once (reuse for all files)
        silence_path = os.path.join(tmp, "silence.mp3")
        subprocess.run(
            ["ffmpeg", "-y",
             "-f", "lavfi", "-i",
             "anullsrc=channel_layout=stereo:sample_rate=" + SAMPLE_RATE,
             "-t", str(SILENCE_S),
             "-b:a", BITRATE, "-c:a", "libmp3lame",
             silence_path],
            capture_output=True, check=True
        )

        for fname in mp3s:
            src = os.path.join(SRC_DIR, fname)
            dst = os.path.join(DST_DIR, fname)
            norm_tmp = os.path.join(tmp, "norm_" + fname)

            print("\n[" + str(ok + fail + 1).zfill(2) + "/" + str(len(mp3s)) + "] " + fname)

            if not two_pass_loudnorm(src, norm_tmp):
                print("  FAILED (loudnorm)")
                fail += 1
                continue

            if not add_silence_pads(norm_tmp, silence_path, dst):
                print("  FAILED (silence concat)")
                fail += 1
                continue

            v = verify_file(dst)
            rms_ok   = v["rms"]  is not None and -23.0 <= v["rms"] <= -18.0
            peak_ok  = v["peak"] is not None and v["peak"] <= -3.0
            lead_ok  = v["leading"]  >= 1.0
            trail_ok = v["trailing"] >= 1.0
            all_ok   = rms_ok and peak_ok and lead_ok and trail_ok

            status = "PASS" if all_ok else "WARN"
            print(
                "  [" + status + "]  "
                + "RMS=" + str(round(v["rms"], 1)) + " dB  "
                + "Peak=" + str(round(v["peak"], 1)) + " dB  "
                + "Lead=" + str(round(v["leading"], 1)) + "s  "
                + "Trail=" + str(round(v["trailing"], 1)) + "s  "
                + str(round(v["dur"] / 60, 1)) + "min"
            )
            if not rms_ok:
                print("    WARNING: RMS out of range!")
            if not peak_ok:
                print("    WARNING: Peak too high!")
            if not lead_ok:
                print("    WARNING: Leading silence < 1s!")
            if not trail_ok:
                print("    WARNING: Trailing silence < 1s!")

            ok += 1

    print("\n" + "=" * 70)
    print("Done: " + str(ok) + " processed, " + str(fail) + " failed.")
    print()
    print("Next steps:")
    print("  1. Run: python ../../check_audio_quality.py final_audio_ar_ready")
    print("  2. Verify all files PASS")
    print("  3. Re-upload to Authors Republic")


if __name__ == "__main__":
    main()
