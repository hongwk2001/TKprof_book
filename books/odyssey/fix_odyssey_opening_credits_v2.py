"""
fix_odyssey_opening_credits_v2.py

Root cause: 2s + 2s silence pads dilute whole-file RMS below -23 dB
for very short (2-3s) credit tracks — and peak is already at ceiling
so simple gain-boost is blocked.

Fix: regenerate the two failing opening credit tracks using 1.0s
silence pads on each side (still within the 1-5s Authors Republic spec).
The 1s padding reduces silence dilution from ~4.2 dB to ~2.6 dB,
keeping the whole-file RMS comfortably within -23 to -18 dB.
"""

import os
import sys
import asyncio
import subprocess
from io import BytesIO
import math

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import edge_tts
from pydub import AudioSegment

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(SCRIPT_DIR, "final_audio")
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

VOICE_EN = "en-US-AndrewNeural"
VOICE_KO = "ko-KR-InJoonNeural"

TARGETS = [
    {
        "fname": "opening_credits_en.mp3",
        "voice": VOICE_EN,
        "text":  "This is The Odyssey: A Spectacular Modern Epic. Written by Homer. Narrated by Andrew.",
    },
    {
        "fname": "opening_credits_ko.mp3",
        "voice": VOICE_KO,
        "text":  "오디세이아: 스펙터클 현대 한국어판입니다. 저자: 호메로스. 낭독: 라이언.",
    },
]

SAMPLE_RATE    = 44100
CHANNELS       = 2
BITRATE        = "256k"
SILENCE_MS     = 1000       # ← 1s each side (reduced from 2s to fix RMS dilution)
TARGET_RMS_DB  = -19.0


async def tts_to_segment(text: str, voice: str) -> AudioSegment:
    for attempt in range(5):
        try:
            communicate = edge_tts.Communicate(text, voice)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            if audio_data:
                return AudioSegment.from_file(BytesIO(audio_data), format="mp3")
        except Exception as e:
            print(f"    Attempt {attempt + 1}/5 failed: {e}")
            await asyncio.sleep(2)
    raise RuntimeError(f"TTS failed: {text[:60]}")


def pad_and_finalize(seg: AudioSegment) -> AudioSegment:
    seg = seg.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)

    # Calculate speech-only RMS target that lands whole-file RMS at TARGET_RMS_DB
    # after adding SILENCE_MS on each side.
    speech_ms = len(seg)
    total_ms  = speech_ms + 2 * SILENCE_MS
    dilution_db = 10 * math.log10(speech_ms / total_ms)
    speech_target = TARGET_RMS_DB - dilution_db  # compensate for silence dilution

    # Normalize speech only
    current_dBFS = seg.dBFS
    if current_dBFS != float("-inf"):
        seg = seg.apply_gain(speech_target - current_dBFS)

    # Safety peak clamp: if normalizing pushed peak over -3.1 dB, pull back
    if seg.max_dBFS > -3.0:
        seg = seg.apply_gain(-(seg.max_dBFS - (-3.1)))

    silence = AudioSegment.silent(duration=SILENCE_MS, frame_rate=SAMPLE_RATE).set_channels(CHANNELS)
    return silence + seg + silence


def export_mp3(seg: AudioSegment, out_path: str):
    seg.export(out_path, format="mp3", bitrate=BITRATE,
               parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {os.path.basename(out_path)}")


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


async def main():
    print("=" * 60)
    print("  Odyssey Opening Credits — Regen Fix (1s silence pads)")
    print("=" * 60)

    all_passed = True
    for t in TARGETS:
        out = os.path.join(OUTPUT_DIR, t["fname"])
        print(f"\n[Regenerating] {t['fname']}")
        print(f"  Voice : {t['voice']}")
        print(f"  Script: {t['text']}")
        raw   = await tts_to_segment(t["text"], t["voice"])
        final = pad_and_finalize(raw)

        speech_ms = len(raw)
        total_ms  = speech_ms + 2 * SILENCE_MS
        dilution  = 10 * math.log10(speech_ms / total_ms)
        print(f"  Speech: {speech_ms/1000:.2f}s | Total: {total_ms/1000:.2f}s | Dilution: {dilution:.1f} dB")

        export_mp3(final, out)
        passed = run_qc(out)
        if not passed:
            all_passed = False

    print(f"\n{'='*60}")
    if all_passed:
        print("  ✅ ALL FIXED FILES NOW PASS QC")
    else:
        print("  ❌ STILL FAILING — see errors above")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
