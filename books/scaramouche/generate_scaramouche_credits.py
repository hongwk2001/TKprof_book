"""
generate_scaramouche_credits.py

Generates:
  - opening_credits_en.mp3 / opening_credits_ko.mp3  (Books 1, 2, 3)
  - closing_credits_en.mp3 / closing_credits_ko.mp3  (Books 1, 2, 3)
  - sample_ko.mp3  (Books 1, 2, 3)  — first 3 min of Chapter 1 KO audio

All files target:
  - 44,100 Hz sample rate
  - 256 kbps CBR MP3
  - ~2s leading + ~2s trailing silence
  - RMS normalized to approx -19 dB
"""

import os
import sys
import asyncio
import subprocess
from io import BytesIO

# Force UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

import edge_tts
from pydub import AudioSegment
from pydub.effects import normalize

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
BOOK_DIRS    = {
    1: os.path.join(SCRIPT_DIR, "final_audio_book1"),
    2: os.path.join(SCRIPT_DIR, "final_audio_book2"),
    3: os.path.join(SCRIPT_DIR, "final_audio_book3"),
}
CHECK_SCRIPT = os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py")

# ── Voices ───────────────────────────────────────────────────────────────────
VOICE_EN = "en-US-AndrewNeural"
VOICE_KO = "ko-KR-SunHiNeural"

# ── Credit Scripts ────────────────────────────────────────────────────────────
CREDITS = {
    1: {
        "en": {
            "opening": "This is Scaramouche, Book One: The Robe. Written by Rafael Sabatini. Narrated by Andrew.",
            "closing": "This has been Scaramouche, Book One: The Robe. Written by Rafael Sabatini. Narrated by Andrew. The End.",
        },
        "ko": {
            "opening": "스카라무슈, 1권: 로브입니다. 저자: 라파엘 사바티니. 낭독: 선희.",
            "closing": "이것으로 스카라무슈 1권: 로브 오디오북을 마칩니다. 저자: 라파엘 사바티니. 낭독: 선희.",
        },
    },
    2: {
        "en": {
            "opening": "This is Scaramouche, Book Two: The Buskin. Written by Rafael Sabatini. Narrated by Andrew.",
            "closing": "This has been Scaramouche, Book Two: The Buskin. Written by Rafael Sabatini. Narrated by Andrew. The End.",
        },
        "ko": {
            "opening": "스카라무슈, 2권: 버스킨입니다. 저자: 라파엘 사바티니. 낭독: 선희.",
            "closing": "이것으로 스카라무슈 2권: 버스킨 오디오북을 마칩니다. 저자: 라파엘 사바티니. 낭독: 선희.",
        },
    },
    3: {
        "en": {
            "opening": "This is Scaramouche, Book Three: The Sword. Written by Rafael Sabatini. Narrated by Andrew.",
            "closing": "This has been Scaramouche, Book Three: The Sword. Written by Rafael Sabatini. Narrated by Andrew. The End.",
        },
        "ko": {
            "opening": "스카라무슈, 3권: 검입니다. 저자: 라파엘 사바티니. 낭독: 선희.",
            "closing": "이것으로 스카라무슈 3권: 검 오디오북을 마칩니다. 저자: 라파엘 사바티니. 낭독: 선희.",
        },
    },
}

# ── Audio constants ───────────────────────────────────────────────────────────
SAMPLE_RATE    = 44100
CHANNELS       = 2          # stereo, matching existing tracks
BITRATE        = "256k"
SILENCE_MS     = 2000       # 2 seconds leading AND trailing
TARGET_RMS_DB  = -19.0      # Authors Republic sweet spot
SAMPLE_CLIP_MS = 3 * 60 * 1000  # 3 minutes for sample


# ── Helpers ───────────────────────────────────────────────────────────────────

async def tts_to_segment(text: str, voice: str) -> AudioSegment:
    """Synthesize text to an AudioSegment via edge-tts (up to 5 retries)."""
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
    raise RuntimeError(f"Failed to synthesize after 5 attempts: {text[:60]}")


def normalize_to_rms(seg: AudioSegment, target_rms_db: float) -> AudioSegment:
    """
    Adjust gain so that the segment's RMS matches target_rms_db.
    Uses pydub's dBFS (which is RMS-based) as a close proxy.
    """
    current_dBFS = seg.dBFS  # pydub dBFS ≈ RMS dBFS
    if current_dBFS == float("-inf"):
        return seg  # silent segment — leave as-is
    gain_needed = target_rms_db - current_dBFS
    return seg.apply_gain(gain_needed)


def pad_and_finalize(seg: AudioSegment) -> AudioSegment:
    """
    1. Normalize RMS to TARGET_RMS_DB
    2. Hard-clip peak to -3.5 dB headroom (apply_gain won't exceed this)
    3. Add SILENCE_MS of silence at start and end
    4. Set to SAMPLE_RATE / CHANNELS
    """
    seg = seg.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)
    seg = normalize_to_rms(seg, TARGET_RMS_DB)

    # Safety clamp: if peak would exceed -3.0 dB after normalization, pull back
    if seg.max_dBFS > -3.0:
        overshoot = seg.max_dBFS - (-3.1)
        seg = seg.apply_gain(-overshoot)

    silence = AudioSegment.silent(duration=SILENCE_MS, frame_rate=SAMPLE_RATE)
    silence = silence.set_channels(CHANNELS)
    return silence + seg + silence


def export_mp3(seg: AudioSegment, out_path: str):
    seg.export(out_path, format="mp3", bitrate=BITRATE,
               parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {os.path.basename(out_path)}")


# ── Main generators ───────────────────────────────────────────────────────────

async def generate_credit_track(book_num: int, lang: str, track_type: str):
    """Generate one opening or closing credit track."""
    voice  = VOICE_EN if lang == "en" else VOICE_KO
    text   = CREDITS[book_num][lang][track_type]
    fname  = f"{track_type}_credits_{lang}.mp3"
    out    = os.path.join(BOOK_DIRS[book_num], fname)

    print(f"\n[Book {book_num} | {lang.upper()} | {track_type.upper()}]")
    print(f"  Script : {text}")
    print(f"  Voice  : {voice}")

    raw = await tts_to_segment(text, voice)
    final = pad_and_finalize(raw)
    export_mp3(final, out)
    return out


def generate_ko_sample(book_num: int):
    """Clip first 3 minutes from final_track_01_ko.mp3 → sample_ko.mp3."""
    src = os.path.join(BOOK_DIRS[book_num], "final_track_01_ko.mp3")
    out = os.path.join(BOOK_DIRS[book_num], "sample_ko.mp3")

    print(f"\n[Book {book_num} | KO | SAMPLE]")
    print(f"  Source : {os.path.basename(src)}")

    if not os.path.exists(src):
        print(f"  ✗ Source not found: {src}")
        return None

    audio = AudioSegment.from_file(src, format="mp3")

    # Trim to 3 minutes (or full track if shorter)
    clip = audio[:SAMPLE_CLIP_MS]

    # Strip existing silence at very start (keep only 2s of ours)
    # Find first non-silent ms (rough: check first 5s)
    clip = clip.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)
    final = pad_and_finalize(clip)
    export_mp3(final, out)
    return out


def run_qc(book_num: int):
    """Run check_audio_quality.py on the book's output directory."""
    book_dir = BOOK_DIRS[book_num]
    check    = os.path.abspath(CHECK_SCRIPT)
    python   = sys.executable

    print(f"\n{'='*60}")
    print(f"  QC CHECK — Book {book_num}: {book_dir}")
    print(f"{'='*60}")

    # Only check the new files to keep output tidy
    new_files = [
        "opening_credits_en.mp3",
        "closing_credits_en.mp3",
        "opening_credits_ko.mp3",
        "closing_credits_ko.mp3",
        "sample_ko.mp3",
    ]

    all_passed = True
    for fname in new_files:
        fpath = os.path.join(book_dir, fname)
        if not os.path.exists(fpath):
            print(f"  [SKIP] {fname} — not found")
            continue
        result = subprocess.run(
            [python, check, fpath],
            capture_output=True, text=True, encoding="utf-8"
        )
        output = result.stdout + result.stderr
        # Print compact result
        for line in output.splitlines():
            if any(kw in line for kw in ["Status:", "Levels:", "Silence:", "Errors:", "PASS", "FAIL", "  -"]):
                print(f"  {line.strip()}")
        if "Status: [FAIL]" in output:
            all_passed = False

    return all_passed


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    print("=" * 60)
    print("  Scaramouche Credits & Sample Generator")
    print("=" * 60)

    generated = []

    # 1. Generate all credit tracks
    for book_num in [1, 2, 3]:
        for lang in ["en", "ko"]:
            for track_type in ["opening", "closing"]:
                path = await generate_credit_track(book_num, lang, track_type)
                generated.append(path)

    # 2. Generate Korean samples
    for book_num in [1, 2, 3]:
        path = generate_ko_sample(book_num)
        if path:
            generated.append(path)

    # 3. QC all output directories
    print("\n\n" + "=" * 60)
    print("  AUTHORS REPUBLIC QC AUDIT")
    print("=" * 60)

    all_books_passed = True
    for book_num in [1, 2, 3]:
        passed = run_qc(book_num)
        if not passed:
            all_books_passed = False

    print("\n" + "=" * 60)
    if all_books_passed:
        print("  ✅ ALL FILES PASSED Authors Republic QC")
    else:
        print("  ❌ SOME FILES FAILED — review errors above and re-run fix_audio_quality.py")
    print("=" * 60)
    print(f"\n  Total files generated: {len(generated)}")
    for p in generated:
        rel = os.path.relpath(p, SCRIPT_DIR)
        print(f"    {rel}")


if __name__ == "__main__":
    asyncio.run(main())
