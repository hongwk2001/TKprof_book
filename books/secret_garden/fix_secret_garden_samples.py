"""
fix_secret_garden_samples.py

Regenerates sample.mp3 for The Secret Garden (both EN and KO).

Root cause of the 2026-09-11 AR rejection ("No end-of-track silence was detected"):

  Measured against the chapter tracks, which AR accepted:
    final_track_02.mp3 : leading 2.00s, trailing 2.00s   -> PASS
    sample.mp3         : leading 2.00s, trailing 4.00s   -> REJECTED

  This script skipped the source's 2s of LEADING silence (SKIP_MS) but never
  trimmed its 2s of TRAILING silence before appending its own 2s pad, so every
  sample shipped with double-length trailing silence. Both EN and KO were hit.

  The pads were also absolute digital zero (-91 dB, literal zero samples).
  authors_republic_requirements.md section 2 warns against this explicitly:
  the silence should carry a natural noise floor, not digital black, because a
  region of pure zeros can be read as absent signal rather than as silence.

Fix strategy:
  1. Skip first 2s of source to bypass any existing leading room noise.
  2. Clip up to 3 minutes of clean speech from that point.
  3. Apply a 2-second fade-out if it hits the 3-minute mark (so it doesn't clip abruptly).
  4. Normalize the speech content to -19 dB RMS.
  5. TRIM the clip's own leading/trailing silence so padding cannot stack.
  6. Pad with 2s of -65 dB room tone (not digital zero) at both ends, which sits
     well under the -60 dB noise-floor ceiling while remaining detectable.
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from pydub import AudioSegment
from pydub.generators import WhiteNoise
from pydub.silence import detect_leading_silence

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

TARGETS = [
    {
        "src": os.path.join(SCRIPT_DIR, "final_audio", "final_track_01.mp3"),
        "out": os.path.join(SCRIPT_DIR, "final_audio", "sample.mp3"),
        "lang": "en"
    },
    {
        "src": os.path.join(SCRIPT_DIR, "final_audio_ko", "final_track_01.mp3"),
        "out": os.path.join(SCRIPT_DIR, "final_audio_ko", "sample.mp3"),
        "lang": "ko"
    }
]

SAMPLE_RATE   = 44100
CHANNELS      = 1               # Secret Garden uses MONO
BITRATE       = "256k"
LEAD_SILENCE  = 2000            # 2s clean digital zero
TRAIL_SILENCE = 2000            # 2s clean digital zero
SKIP_MS       = 2000            # skip first 2s of source
CLIP_MS       = 3 * 60 * 1000   # max 3 minutes
TARGET_RMS_DB = -19.0


ROOM_TONE_DB = -65.0            # under the -60 dB noise-floor ceiling
TRIM_THRESHOLD_DB = -50.0


def normalize_to_rms(seg: AudioSegment, target_db: float) -> AudioSegment:
    if seg.dBFS == float("-inf"):
        return seg
    return seg.apply_gain(target_db - seg.dBFS)


def strip_edge_silence(seg: AudioSegment) -> AudioSegment:
    """
    Remove the clip's own leading/trailing silence.

    Without this the source's existing 2s tail stacks with the pad we add,
    which is what produced the 4s trailing silence AR rejected.
    """
    lead = detect_leading_silence(seg, silence_threshold=TRIM_THRESHOLD_DB,
                                  chunk_size=10)
    trail = detect_leading_silence(seg.reverse(),
                                   silence_threshold=TRIM_THRESHOLD_DB,
                                   chunk_size=10)
    if lead + trail >= len(seg):
        return seg
    return seg[lead:len(seg) - trail]


def room_tone(duration_ms: int) -> AudioSegment:
    """Near-inaudible noise floor. AR wants room tone, not digital zero."""
    return (WhiteNoise()
            .to_audio_segment(duration=duration_ms, volume=ROOM_TONE_DB)
            .set_frame_rate(SAMPLE_RATE)
            .set_channels(CHANNELS))


def build_sample(src_path: str, out_path: str) -> bool:
    if not os.path.exists(src_path):
        print(f"  ✗ Source not found: {src_path}")
        return False

    print(f"  Loading: {src_path}")
    audio = AudioSegment.from_file(src_path, format="mp3")

    # Skip first 2s to skip leading room-noise
    content = audio[SKIP_MS:] if len(audio) > SKIP_MS else audio
    
    # Clip max 3 minutes
    clip = content[:CLIP_MS]
    
    # Fade out if we actually truncated the audio (smooth sample ending)
    if len(clip) == CLIP_MS:
        clip = clip.fade_out(2000)

    clip = clip.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)

    # Normalize SPEECH ONLY
    clip = normalize_to_rms(clip, TARGET_RMS_DB)
    
    # Safety peak clamp
    if clip.max_dBFS > -3.0:
        clip = clip.apply_gain(-(clip.max_dBFS - (-3.1)))

    # Trim the clip's OWN silence so the pads below cannot stack on top of it
    clip = strip_edge_silence(clip)
    clip = clip.fade_out(150)          # avoid a click into the pad

    # Pad with room tone (not digital zero) AFTER normalization
    final = room_tone(LEAD_SILENCE) + clip + room_tone(TRAIL_SILENCE)

    final.export(out_path, format="mp3", bitrate=BITRATE,
                 parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {out_path}")
    return True


def run_qc(fpath: str) -> bool:
    result = subprocess.run(
        [sys.executable, CHECK_SCRIPT, fpath],
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
    print("  Secret Garden Sample Fix (Clean Silence Pads)")
    print("=" * 60)

    generated = []
    all_passed = True

    for t in TARGETS:
        print(f"\n[SAMPLE | {t['lang'].upper()}]")
        if build_sample(t["src"], t["out"]):
            generated.append(t["out"])

    print(f"\n\n{'='*60}")
    print("  QC AUDIT — Regenerated Samples")
    print(f"{'='*60}")

    for fpath in generated:
        if not run_qc(fpath):
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("  ✅ ALL SAMPLES PASSED QC")
    else:
        print("  ❌ SOME FAILED — see above")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
