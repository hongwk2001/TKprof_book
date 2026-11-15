"""
generate_secret_garden_credits.py

Generates for The Secret Garden audiobook:
  final_audio/opening_credits_en.mp3
  final_audio/closing_credits_en.mp3
  final_audio_ko/opening_credits_ko.mp3
  final_audio_ko/closing_credits_ko.mp3

EN voice: Kokoro af_sarah (→ narrator name "Sarah")
         Falls back to edge-tts en-GB-SoniaNeural if Kokoro unavailable
KO voice: edge-tts ko-KR-SunHiNeural (→ narrator name "선희")

All files:
  - MONO (1ch) to match existing tracks
  - 44,100 Hz, 256 kbps CBR
  - 1s leading + 1s trailing silence (short-track safe)
  - Dilution-compensated RMS normalization → whole-file RMS in -23..-18 dB range
"""

import os
import sys
import asyncio
import subprocess
import math
from io import BytesIO

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from pydub import AudioSegment

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
EN_OUT_DIR   = os.path.join(SCRIPT_DIR, "final_audio")
KO_OUT_DIR   = os.path.join(SCRIPT_DIR, "final_audio_ko")
CHECK_SCRIPT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "check_audio_quality.py"))

# ── Voice config ───────────────────────────────────────────────────────────────
KOKORO_VOICE   = "af_sarah"         # Kokoro American Female Sarah
FALLBACK_VOICE = "en-GB-SoniaNeural" # edge-tts fallback
KO_VOICE       = "ko-KR-SunHiNeural"

# ── Credit scripts ─────────────────────────────────────────────────────────────
CREDITS = {
    "en": {
        "opening": "This is The Secret Garden: A Modernized Classic for Casual Readers and ESL Learners. Written by Frances Hodgson Burnett. Narrated by Sarah.",
        "closing": "This has been The Secret Garden: A Modernized Classic for Casual Readers and ESL Learners. Written by Frances Hodgson Burnett. Narrated by Sarah. The End.",
    },
    "ko": {
        "opening": "비밀의 화원: 현대인을 위한 감성 힐링 클래식입니다. 저자: 프랜시스 호지슨 버넷. 낭독: 선희.",
        "closing": "이것으로 비밀의 화원: 현대인을 위한 감성 힐링 클래식 오디오북을 마칩니다. 저자: 프랜시스 호지슨 버넷. 낭독: 선희.",
    },
}

# ── Audio constants ────────────────────────────────────────────────────────────
SAMPLE_RATE   = 44100
CHANNELS      = 1           # MONO — matches all existing Secret Garden tracks
BITRATE       = "256k"
SILENCE_MS    = 1000        # 1s pads (short-track safe, within 1-5s spec)
TARGET_RMS_DB = -19.0


# ── Kokoro EN synthesis ────────────────────────────────────────────────────────

def try_kokoro(text: str) -> AudioSegment | None:
    """Attempt to synthesize with Kokoro af_sarah. Returns None on failure."""
    try:
        import numpy as np
        import soundfile as sf
        from kokoro import KPipeline

        print(f"  [Kokoro] Synthesizing with {KOKORO_VOICE}...")
        pipeline = KPipeline(lang_code="a")
        segments = []
        for _, _, audio in pipeline(text, voice=KOKORO_VOICE, speed=1.0):
            if audio is not None and len(audio) > 0:
                segments.append(audio)
        if not segments:
            return None

        import numpy as np
        merged = np.concatenate(segments)

        # Write to temp WAV then load as AudioSegment
        tmp_wav = os.path.join(SCRIPT_DIR, "_tmp_credits.wav")
        sf.write(tmp_wav, merged, 24000)
        seg = AudioSegment.from_wav(tmp_wav)
        os.remove(tmp_wav)
        return seg
    except Exception as e:
        print(f"  [Kokoro] Not available ({e}), falling back to edge-tts...")
        return None


# ── edge-tts synthesis ─────────────────────────────────────────────────────────

async def tts_edgetts(text: str, voice: str) -> AudioSegment:
    import edge_tts
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
            print(f"    Attempt {attempt+1}/5 failed: {e}")
            await asyncio.sleep(2)
    raise RuntimeError(f"edge-tts failed after 5 attempts: {text[:60]}")


# ── Audio processing ───────────────────────────────────────────────────────────

def pad_and_finalize(seg: AudioSegment) -> AudioSegment:
    """
    Normalize with dilution compensation, then add silence pads.
    Compensates for the RMS drop caused by silence padding on short tracks.
    """
    seg = seg.set_frame_rate(SAMPLE_RATE).set_channels(CHANNELS)

    speech_ms = len(seg)
    total_ms  = speech_ms + 2 * SILENCE_MS
    # How much silence will dilute the RMS
    dilution_db   = 10 * math.log10(speech_ms / total_ms)
    speech_target = TARGET_RMS_DB - dilution_db   # compensate

    current_dBFS = seg.dBFS
    if current_dBFS != float("-inf"):
        seg = seg.apply_gain(speech_target - current_dBFS)

    # Safety peak clamp to -3.1 dB
    if seg.max_dBFS > -3.0:
        seg = seg.apply_gain(-(seg.max_dBFS - (-3.1)))

    silence = AudioSegment.silent(duration=SILENCE_MS,
                                  frame_rate=SAMPLE_RATE).set_channels(CHANNELS)
    padded = silence + seg + silence
    print(f"    Speech: {speech_ms/1000:.2f}s | Total: {total_ms/1000:.2f}s"
          f" | Dilution comp: {dilution_db:+.1f} dB")
    return padded


def export_mp3(seg: AudioSegment, out_path: str):
    seg.export(out_path, format="mp3", bitrate=BITRATE,
               parameters=["-ar", str(SAMPLE_RATE)])
    print(f"  ✔ Exported: {os.path.basename(out_path)}")


# ── QC ─────────────────────────────────────────────────────────────────────────

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


# ── Main ───────────────────────────────────────────────────────────────────────

async def main():
    print("=" * 60)
    print("  Secret Garden Credits Generator")
    print("=" * 60)

    generated = []

    # ── EN OPENING ─────────────────────────────────────────────────────────────
    print(f"\n[EN | OPENING]")
    print(f"  Script: {CREDITS['en']['opening']}")
    seg = try_kokoro(CREDITS["en"]["opening"])
    if seg is None:
        print(f"  Using edge-tts fallback: {FALLBACK_VOICE}")
        seg = await tts_edgetts(CREDITS["en"]["opening"], FALLBACK_VOICE)
    out = os.path.join(EN_OUT_DIR, "opening_credits_en.mp3")
    export_mp3(pad_and_finalize(seg), out)
    generated.append(out)

    # ── EN CLOSING ─────────────────────────────────────────────────────────────
    print(f"\n[EN | CLOSING]")
    print(f"  Script: {CREDITS['en']['closing']}")
    seg = try_kokoro(CREDITS["en"]["closing"])
    if seg is None:
        seg = await tts_edgetts(CREDITS["en"]["closing"], FALLBACK_VOICE)
    out = os.path.join(EN_OUT_DIR, "closing_credits_en.mp3")
    export_mp3(pad_and_finalize(seg), out)
    generated.append(out)

    # ── KO OPENING ─────────────────────────────────────────────────────────────
    print(f"\n[KO | OPENING]")
    print(f"  Script: {CREDITS['ko']['opening']}")
    seg = await tts_edgetts(CREDITS["ko"]["opening"], KO_VOICE)
    out = os.path.join(KO_OUT_DIR, "opening_credits_ko.mp3")
    export_mp3(pad_and_finalize(seg), out)
    generated.append(out)

    # ── KO CLOSING ─────────────────────────────────────────────────────────────
    print(f"\n[KO | CLOSING]")
    print(f"  Script: {CREDITS['ko']['closing']}")
    seg = await tts_edgetts(CREDITS["ko"]["closing"], KO_VOICE)
    out = os.path.join(KO_OUT_DIR, "closing_credits_ko.mp3")
    export_mp3(pad_and_finalize(seg), out)
    generated.append(out)

    # ── QC AUDIT ───────────────────────────────────────────────────────────────
    print(f"\n\n{'='*60}")
    print("  AUTHORS REPUBLIC QC AUDIT")
    print(f"{'='*60}")

    all_passed = True
    for fpath in generated:
        if not run_qc(fpath):
            all_passed = False

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
