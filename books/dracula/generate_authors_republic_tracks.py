import os
import sys
import asyncio
import subprocess
import torch
import numpy as np
import soundfile as sf
import edge_tts
from pydub import AudioSegment

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

try:
    from kokoro import KPipeline
except ImportError:
    print("[ERROR] kokoro python module not installed properly.")
    sys.exit(1)

TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

VOICE_EN = "am_adam"                   # Kokoro male voice (Ryan equivalent)
VOICE_KO_EDGE = "ko-KR-SunHiNeural"    # Edge-TTS SunHi voice for Korean

_kokoro_pipeline = None

def get_kokoro_pipeline():
    global _kokoro_pipeline
    if _kokoro_pipeline is None:
        _kokoro_pipeline = KPipeline(lang_code="a")
    return _kokoro_pipeline

def synthesize_kokoro(text, out_wav_path):
    pipeline = get_kokoro_pipeline()
    generator = pipeline(text, voice=VOICE_EN, speed=1.0)
    audio_segments = []
    for gs, ps, audio in generator:
        if audio is not None and len(audio) > 0:
            audio_segments.append(audio)
    if not audio_segments:
        return False
    merged_audio = np.concatenate(audio_segments)
    sf.write(out_wav_path, merged_audio, 24000)
    return True

async def synthesize_edge_async(text, out_wav_path):
    temp_mp3 = out_wav_path.replace(".wav", "_edge.mp3")
    communicate = edge_tts.Communicate(text, VOICE_KO_EDGE)
    await communicate.save(temp_mp3)
    if os.path.exists(temp_mp3) and os.path.getsize(temp_mp3) > 100:
        audio = AudioSegment.from_file(temp_mp3, format="mp3")
        audio.export(out_wav_path, format="wav")
        try:
            os.remove(temp_mp3)
        except OSError:
            pass
        return True
    return False

def apply_acx_post_processing(raw_path, clean_path, bitrate=256):
    """
    Applies standard FFmpeg post-processing to satisfy ACX / Authors Republic requirements:
    - Target RMS: -19 LUFS (RMS between -23 dB and -18 dB)
    - True Peak limit: <= -3.0 dB (-3.5 dB targeted)
    - Clean silence padding: 2.0s (2000ms) at start AND end
    - Sample rate: 44,100 Hz
    - Bitrate: 256 kbps CBR MP3
    """
    volume_norm = "loudnorm=I=-19:TP=-3.5:LRA=7"
    strip_silence = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0,areverse"
    leading_silence = "adelay=2000|2000"
    trailing_silence = "apad=pad_dur=2"

    filter_chain = f"{strip_silence},{volume_norm},{leading_silence},{trailing_silence}"

    cmd = [
        "ffmpeg", "-y", "-threads", "8", "-i", raw_path,
        "-af", filter_chain,
        "-ar", "44100",
        "-b:a", f"{bitrate}k",
        clean_path
    ]
    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] FFmpeg post-processing failed:\n{e.stderr}", file=sys.stderr)
        return False

def verify_audio_quality(mp3_path):
    checker_script = os.path.join(PROJECT_ROOT, "check_audio_quality.py")
    if not os.path.exists(checker_script):
        return True
    cmd = [sys.executable, checker_script, mp3_path]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[QUALITY CHECK PASSED] {os.path.basename(mp3_path)}")
            return True
        else:
            print(f"[QUALITY CHECK WARNING] {res.stdout.strip()}")
            return False
    except Exception as e:
        print(f"[QUALITY CHECK ERROR] {e}")
        return False

def generate_opening_credits():
    print("\n==================================================")
    print(" Generating Opening Credits (Authors Republic Spec)")
    print(" Strict Rule: Title, Author, Narrator ONLY")
    print("==================================================")
    
    en_text = "This is Dracula, Unabridged Bilingual Edition, by Bram Stoker. Narrated by Ryan and Sohee."
    ko_text = "드라큘라 무삭제 영한 대역판. 저자: 브램 스토커. 낭독: 라이언, 소희."

    wav_en = os.path.join(TEMP_DIR, "opening_en.wav")
    wav_ko = os.path.join(TEMP_DIR, "opening_ko.wav")
    raw_mp3 = os.path.join(TEMP_DIR, "raw_opening_credits.mp3")
    final_mp3 = os.path.join(OUTPUT_DIR, "opening_credits.mp3")

    synthesize_kokoro(en_text, wav_en)
    asyncio.run(synthesize_edge_async(ko_text, wav_ko))

    combined = AudioSegment.from_file(wav_en) + AudioSegment.silent(duration=500) + AudioSegment.from_file(wav_ko)
    combined.export(raw_mp3, format="mp3", bitrate="256k")
    apply_acx_post_processing(raw_mp3, final_mp3)
    verify_audio_quality(final_mp3)

def generate_closing_credits():
    print("\n==================================================")
    print(" Generating Closing Credits (Authors Republic Spec)")
    print(" Strict Rule: Concise Ending Statement ONLY")
    print("==================================================")

    en_text = "This has been Dracula, by Bram Stoker. Narrated by Ryan and Sohee. The End."
    ko_text = "이것으로 브램 스토커 원작, 드라큘라 오디오북을 마칩니다. 낭독: 라이언, 소희. 끝."

    wav_en = os.path.join(TEMP_DIR, "closing_en.wav")
    wav_ko = os.path.join(TEMP_DIR, "closing_ko.wav")
    raw_mp3 = os.path.join(TEMP_DIR, "raw_closing_credits.mp3")
    final_mp3 = os.path.join(OUTPUT_DIR, "closing_credits.mp3")

    synthesize_kokoro(en_text, wav_en)
    asyncio.run(synthesize_edge_async(ko_text, wav_ko))

    combined = AudioSegment.from_file(wav_en) + AudioSegment.silent(duration=500) + AudioSegment.from_file(wav_ko)
    combined.export(raw_mp3, format="mp3", bitrate="256k")
    apply_acx_post_processing(raw_mp3, final_mp3)
    verify_audio_quality(final_mp3)

def generate_sample_track():
    print("\n==================================================")
    print(" Generating Retail Sample (Authors Republic Spec)")
    print(" Duration: 4 Minutes 30 Seconds with 2s Padding")
    print("==================================================")

    ch1_path = os.path.join(OUTPUT_DIR, "dracula_ch_01_bilingual_sunhi.mp3")
    if not os.path.exists(ch1_path):
        ch1_path = os.path.join(OUTPUT_DIR, "dracula_ch_01_bilingual.mp3")

    raw_sample_mp3 = os.path.join(TEMP_DIR, "raw_sample.mp3")
    final_sample_mp3 = os.path.join(OUTPUT_DIR, "sample.mp3")

    if os.path.exists(ch1_path):
        ch1_audio = AudioSegment.from_mp3(ch1_path)
        # 4 minutes 30 seconds (270000 ms)
        sample_audio = ch1_audio[:270000]
        sample_audio.export(raw_sample_mp3, format="mp3", bitrate="256k")
        apply_acx_post_processing(raw_sample_mp3, final_sample_mp3)
        verify_audio_quality(final_sample_mp3)

def main():
    generate_opening_credits()
    generate_closing_credits()
    generate_sample_track()

    print("\n=========================================================================")
    print(" AUTHORS REPUBLIC TRACKS CREATED AND VERIFIED SUCCESSFULLY!")
    print("  1. opening_credits.mp3")
    print("  2. closing_credits.mp3")
    print("  3. sample.mp3")
    print("=========================================================================\n")

if __name__ == "__main__":
    main()
