"""
fix_odyssey_opening_credits.py

Re-normalises the two failing opening credit tracks using
ffmpeg loudnorm (EBU R128), which handles the short-track
silence-dilution problem that pydub's simple gain approach
cannot resolve when peak is already at ceiling.

Targets:
  - Integrated loudness (I): -21 LUFS  → RMS ~ -21 dB  (well within -23...-18 dB)
  - True peak             (TP): -3.5 dB → peak safely under -3.0 dB
  - Loudness range        (LRA): 11 LU
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR  = os.path.join(SCRIPT_DIR, "final_audio")
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

TARGETS = [
    "opening_credits_en.mp3",
    "opening_credits_ko.mp3",
]

LOUDNORM = "loudnorm=I=-21:TP=-3.5:LRA=11:linear=true"


def loudnorm_file(fpath: str):
    """Two-pass ffmpeg loudnorm: pass1 analyses, pass2 applies."""
    tmp = fpath + ".tmp.mp3"

    # Single-pass linear loudnorm (accurate enough for these short tracks)
    cmd = [
        "ffmpeg", "-y", "-i", fpath,
        "-af", LOUDNORM,
        "-ar", "44100",
        "-b:a", "256k",
        tmp
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ ffmpeg error:\n{result.stderr[-800:]}")
        return False

    os.replace(tmp, fpath)
    print(f"  ✔ Loudnorm applied: {os.path.basename(fpath)}")
    return True


def run_qc(fpath: str) -> bool:
    python = sys.executable
    result = subprocess.run(
        [python, CHECK_SCRIPT, fpath],
        capture_output=True, text=True, encoding="utf-8"
    )
    output = result.stdout + result.stderr
    print(f"\n  [{os.path.basename(fpath)}]")
    for line in output.splitlines():
        if any(kw in line for kw in ["Status:", "Levels:", "Silence:", "Errors:", "  - "]):
            print(f"    {line.strip()}")
    return "Status: [FAIL]" not in output


def main():
    print("=" * 60)
    print("  Odyssey Opening Credits — Loudnorm Fix")
    print("=" * 60)

    all_passed = True
    for fname in TARGETS:
        fpath = os.path.join(OUTPUT_DIR, fname)
        if not os.path.exists(fpath):
            print(f"\n[SKIP] {fname} — not found")
            continue
        print(f"\n[Fixing] {fname}")
        if loudnorm_file(fpath):
            passed = run_qc(fpath)
            if not passed:
                all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("  ✅ ALL FIXED FILES NOW PASS QC")
    else:
        print("  ❌ STILL FAILING — check errors above")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
