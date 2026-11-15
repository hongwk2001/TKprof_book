"""
generate_odyssey_credits.py

Generates for The Odyssey (오디세이아) audiobook:
  - opening_credits_en.mp3   (en-US-AndrewNeural → "Andrew")
  - closing_credits_en.mp3
  - opening_credits_ko.mp3   (ko-KR-InJoonNeural → "라이언")
  - closing_credits_ko.mp3
  - sample_en.mp3            (first 3 min of final_track_01.mp3)
  - sample_ko.mp3            (first 3 min of final_track_ko_01.mp3)

All files target:
  - 44,100 Hz, 256 kbps CBR MP3
  - ~2s leading + ~2s trailing silence
  - RMS normalized to approx -19 dB
"""

import os
import sys
import asyncio
import subprocess
from io import BytesIO

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import edge_tts
from pydub import AudioSegment

# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR   = os.path.join(SCRIPT_DIR, "final_audio")
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

# ── Voices ────────────────────────────────────────────────────────────────────
VOICE_EN = "en-US-AndrewNeural"   # Narrator name in credits: "Andrew"
VOICE_KO = "ko-KR-InJoonNeural"   # Narrator name in credits: "라이언"

# ── Credit Scripts ─────────────────────────────────────────────────────────────
CREDITS = {
    "en": {
        "title":   "The Odyssey: A Spectacular Modern Epic",
        "author":  "Homer",
        "narrator":"Andrew",
        "opening": "This is The Odyssey: A Spectacular Modern Epic. Written by Homer. Narrated by Andrew.",
        "closing": "This has been The Odyssey: A Spectacular Modern Epic. Written by Homer. Narrated by Andrew. The End.",
    },
    "ko": {
        "title":   "오디세이아: 스펙터클 현대 한국어판",
        "author":  "호메로스",
        "narrator":"라이언",
        "opening": "오디세이아: 스펙터클 현대 한국어판입니다. 저자: 호메로스. 낭독: 라이언.",
        "closing": "이것으로 오디세이아: 스펙터클 현대 한국어판 오디오북을 마칩니다. 저자: 호메로스. 낭독: 라이언.",
    },
}

# ── Audio constants ───────────────────────────────────────────────────────────
SAMPLE_RATE   = 44100
CHANNELS      = 2
BITRATE       = "256k"
SILENCE_MS    = 2000       # 2s leading + 2s trailing
TARGET_RMS_DB = -19.0
SAMPLE_CLIP_MS = 3 * 60 * 1000  # 3 minutes


# ── Helpers ───────────────────────────────────────────────────────────────────

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
    raise RuntimeError(f"TTS failed after 5 attempts: {text[:60]}")


def normalize_to_rms(seg: AudioSegment, target_rms_db: float) -> AudioSegment:
    current_dBFS = seg.dBFS
    if current_dBFS == float("-inf"):
        return seg
    return seg.apply_gain(target_rms_db - current_dBFS)


def pad_and_finalize(seg: AudioSegment) -> AudioSegment:
    seg = seg.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)
    seg = normalize_to_rms(seg, TARGET_RMS_DB)
    # Safety clamp peak to -3.1 dB
    if seg.max_dBFS > -3.0:
        seg = seg.apply_gain(-(seg.max_dBFS - (-3.1)))
    silence = AudioSegment.silent(duration=SILENCE_MS, frame_rate=SAMPLE_RATE).set_channels(CHANNELS)
    return silence + seg + silence


def export_mp3(seg: AudioSegment, out_path: str):
    seg.export(out_path, format="mp3", bitrate=BITRATE,
               parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {os.path.basename(out_path)}")


# ── Generators ────────────────────────────────────────────────────────────────

async def generate_credit_track(lang: str, track_type: str):
    voice = VOICE_EN if lang == "en" else VOICE_KO
    text  = CREDITS[lang][track_type]
    fname = f"{track_type}_credits_{lang}.mp3"
    out   = os.path.join(OUTPUT_DIR, fname)

    print(f"\n[{lang.upper()} | {track_type.upper()}]")
    print(f"  Script : {text}")
    print(f"  Voice  : {voice}")

    raw   = await tts_to_segment(text, voice)
    final = pad_and_finalize(raw)
    export_mp3(final, out)
    return out


def generate_sample(lang: str):
    if lang == "en":
        src   = os.path.join(OUTPUT_DIR, "final_track_01.mp3")
        fname = "sample_en.mp3"
    else:
        src   = os.path.join(OUTPUT_DIR, "final_track_ko_01.mp3")
        fname = "sample_ko.mp3"

    out = os.path.join(OUTPUT_DIR, fname)
    print(f"\n[{lang.upper()} | SAMPLE]")
    print(f"  Source : {os.path.basename(src)}")

    if not os.path.exists(src):
        print(f"  ✗ Source not found: {src}")
        return None

    audio = AudioSegment.from_file(src, format="mp3")
    clip  = audio[:SAMPLE_CLIP_MS]
    final = pad_and_finalize(clip)
    export_mp3(final, out)
    return out


def run_qc(files: list):
    print(f"\n\n{'='*60}")
    print("  AUTHORS REPUBLIC QC AUDIT")
    print(f"{'='*60}")

    python = sys.executable
    all_passed = True

    for fpath in files:
        if not fpath or not os.path.exists(fpath):
            print(f"  [SKIP] {fpath} — not found")
            continue
        result = subprocess.run(
            [python, CHECK_SCRIPT, fpath],
            capture_output=True, text=True, encoding="utf-8"
        )
        output = result.stdout + result.stderr
        fname  = os.path.basename(fpath)
        print(f"\n  [{fname}]")
        for line in output.splitlines():
            if any(kw in line for kw in ["Status:", "Levels:", "Silence:", "Errors:", "  - "]):
                print(f"    {line.strip()}")
        if "Status: [FAIL]" in output:
            all_passed = False

    return all_passed


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    print("=" * 60)
    print("  Odyssey Credits & Sample Generator")
    print("=" * 60)

    generated = []

    # 1. Credit tracks: EN + KO, opening + closing
    for lang in ["en", "ko"]:
        for track_type in ["opening", "closing"]:
            path = await generate_credit_track(lang, track_type)
            generated.append(path)

    # 2. Samples: EN (refresh existing) + KO (new)
    for lang in ["en", "ko"]:
        path = generate_sample(lang)
        if path:
            generated.append(path)

    # 3. QC audit
    all_passed = run_qc(generated)

    print(f"\n{'='*60}")
    if all_passed:
        print("  ✅ ALL FILES PASSED Authors Republic QC")
    else:
        print("  ❌ SOME FILES FAILED — see errors above")
    print(f"{'='*60}")

    print(f"\n  Total files generated: {len(generated)}")
    for p in generated:
        print(f"    {os.path.relpath(p, SCRIPT_DIR)}")


if __name__ == "__main__":
    asyncio.run(main())
