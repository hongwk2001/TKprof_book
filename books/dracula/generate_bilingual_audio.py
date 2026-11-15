import os
import sys
import json
import re
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

# Path setup for Qwen3-TTS
QWEN3_TTS_DIR = os.path.join(PROJECT_ROOT, "Qwen3-TTS")
if QWEN3_TTS_DIR not in sys.path:
    sys.path.insert(0, QWEN3_TTS_DIR)

try:
    from kokoro import KPipeline
except ImportError:
    print("[ERROR] kokoro python module not installed properly.")
    sys.exit(1)

SCRIPTS_DIR = os.path.join(SCRIPT_DIR, "scripts")
TEMP_DIR = os.path.join(SCRIPT_DIR, "temp_audio")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "final_audio")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Device Configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Voice Configuration
VOICE_EN = "am_adam"                   # Kokoro male voice (Ryan equivalent in Kokoro)
VOICE_KO_EDGE = "ko-KR-SunHiNeural"    # Edge-TTS SunHi voice for Korean
VOICE_KO_QWEN = "sohee"                # Qwen3-TTS custom voice for Korean

# Global Model Singletons
_kokoro_pipeline = None
_qwen_model = None

def get_kokoro_pipeline():
    global _kokoro_pipeline
    if _kokoro_pipeline is None:
        print("[INIT] Loading Kokoro TTS Pipeline (EN)...")
        _kokoro_pipeline = KPipeline(lang_code="a")
    return _kokoro_pipeline

def get_qwen_model():
    global _qwen_model
    if _qwen_model is None:
        print("[INIT] Loading Qwen3-TTS Model on CUDA (KO)...")
        from qwen_tts import Qwen3TTSModel
        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        _qwen_model = Qwen3TTSModel.from_pretrained(
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
            device_map="cuda:0" if DEVICE == "cuda" else "cpu",
            dtype=dtype,
            attn_implementation="sdpa"
        )
    return _qwen_model

def create_silence_audio(duration_ms=500):
    return AudioSegment.silent(duration=duration_ms)

def synthesize_kokoro_segment(text, voice_name, out_wav_path):
    """Synthesizes English segment using Kokoro TTS."""
    if not re.search(r"[a-zA-Z0-9]", text):
        create_silence_audio(500).export(out_wav_path, format="wav")
        return True

    pipeline = get_kokoro_pipeline()
    generator = pipeline(text, voice=voice_name, speed=1.0)
    
    audio_segments = []
    for gs, ps, audio in generator:
        if audio is not None and len(audio) > 0:
            audio_segments.append(audio)

    if not audio_segments:
        create_silence_audio(500).export(out_wav_path, format="wav")
        return True

    merged_audio = np.concatenate(audio_segments)
    sf.write(out_wav_path, merged_audio, 24000)
    return True

async def synthesize_edge_segment_async(text, voice_name, out_wav_path):
    """Synthesizes Korean segment using Edge-TTS (SunHi)."""
    if not re.search(r"[\uac00-\ud7a3a-zA-Z0-9]", text):
        create_silence_audio(500).export(out_wav_path, format="wav")
        return True

    temp_mp3 = out_wav_path.replace(".wav", "_edge.mp3")
    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(text, voice_name)
            await communicate.save(temp_mp3)
            if os.path.exists(temp_mp3) and os.path.getsize(temp_mp3) > 100:
                audio = AudioSegment.from_file(temp_mp3, format="mp3")
                audio.export(out_wav_path, format="wav")
                try:
                    os.remove(temp_mp3)
                except OSError:
                    pass
                return True
        except Exception as e:
            print(f"    [RETRY {attempt+1}] Edge-TTS error: {e}")
            await asyncio.sleep(1)

    create_silence_audio(500).export(out_wav_path, format="wav")
    return True

def synthesize_qwen_segment(text, speaker_name, out_wav_path):
    """Synthesizes Korean segment using Qwen3-TTS."""
    if not re.search(r"[\uac00-\ud7a3a-zA-Z0-9]", text):
        create_silence_audio(500).export(out_wav_path, format="wav")
        return True

    model = get_qwen_model()
    wavs, sr = model.generate_custom_voice(
        text=text,
        language="Korean",
        speaker=speaker_name
    )

    audio_data = wavs[0]
    if isinstance(audio_data, torch.Tensor):
        audio_data = audio_data.cpu().numpy()

    sf.write(out_wav_path, audio_data, sr)
    return True

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
    """Runs check_audio_quality.py script on the output file."""
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

def generate_bilingual_chapter(ch_num, ko_engine="edge"):
    ch_str = f"{ch_num:02d}"
    script_file = os.path.join(SCRIPTS_DIR, f"bilingual_ch_{ch_str}.json")

    if not os.path.exists(script_file):
        print(f"[ERROR] Bilingual script file not found: {script_file}")
        return False

    with open(script_file, "r", encoding="utf-8") as f:
        items = json.load(f)

    folder_name = f"ch_{ch_str}_sunhi" if ko_engine == "edge" else f"ch_{ch_str}"
    ch_temp_dir = os.path.join(TEMP_DIR, folder_name)
    os.makedirs(ch_temp_dir, exist_ok=True)

    suffix = "_sunhi" if ko_engine == "edge" else ""
    raw_mp3_path = os.path.join(TEMP_DIR, f"raw_ch_{ch_str}_bilingual{suffix}.mp3")
    final_mp3_path = os.path.join(OUTPUT_DIR, f"dracula_ch_{ch_str}_bilingual{suffix}.mp3")

    ko_voice_desc = f"Edge-TTS ({VOICE_KO_EDGE})" if ko_engine == "edge" else f"Qwen3 ({VOICE_KO_QWEN})"

    print(f"\n==================================================")
    print(f" Processing Dracula Chapter {ch_str} Bilingual Audio")
    print(f" Segments: {len(items)} | EN Voice: Kokoro ({VOICE_EN}) | KO Voice: {ko_voice_desc}")
    print(f"==================================================")

    # 1. Synthesize individual paragraph WAVs with cache checking
    para_files = []
    generated_count = 0
    cached_count = 0

    for idx, item in enumerate(items):
        tag = item["tag"]
        lang = item["lang"]
        text = item["text"].strip()

        wav_filename = f"{tag}_{lang}.wav"
        wav_path = os.path.join(ch_temp_dir, wav_filename)
        para_files.append((tag, lang, wav_path))

        # RESUME CHECK: Skip if file exists and has size > 100 bytes
        if os.path.exists(wav_path) and os.path.getsize(wav_path) > 100:
            cached_count += 1
            continue

        print(f" [{idx+1}/{len(items)}] Synthesizing [{tag}_{lang.upper()}]: {text[:30]}...")

        try:
            if lang == "en":
                success = synthesize_kokoro_segment(text, VOICE_EN, wav_path)
            else:
                if ko_engine == "edge":
                    success = asyncio.run(synthesize_edge_segment_async(text, VOICE_KO_EDGE, wav_path))
                else:
                    success = synthesize_qwen_segment(text, VOICE_KO_QWEN, wav_path)

            if not success:
                print(f"  [ERROR] Failed to synthesize [{tag}_{lang}]")
                return False
            generated_count += 1

        except Exception as e:
            print(f"  [EXCEPT] Error synthesizing [{tag}_{lang}]: {e}")
            return False

    print(f"\n[CACHE SUMMARY] Chapter {ch_str}: {cached_count} loaded from cache, {generated_count} newly synthesized.")

    # 2. Stitch paragraph WAVs in interleaved order
    print(f"Stitching {len(para_files)} paragraph segments into raw master track...")
    combined_audio = AudioSegment.empty()
    en_ko_pause = AudioSegment.silent(duration=350)  # 350ms pause between EN and KO
    para_pause = AudioSegment.silent(duration=500)   # 500ms pause between paragraphs

    for i, (tag, lang, wav_path) in enumerate(para_files):
        if not os.path.exists(wav_path):
            print(f"[ERROR] Missing segment file during stitching: {wav_path}")
            return False

        seg_audio = AudioSegment.from_file(wav_path)
        combined_audio += seg_audio

        if lang == "en":
            combined_audio += en_ko_pause
        else:
            combined_audio += para_pause

    print(f"Exporting un-processed raw track to {raw_mp3_path}...")
    combined_audio.export(raw_mp3_path, format="mp3", bitrate="256k")

    # 3. Apply ACX / Authors Republic FFmpeg post-processing
    print(f"Applying ACX/Authors Republic post-processing to {final_mp3_path}...")
    success = apply_acx_post_processing(raw_mp3_path, final_mp3_path, bitrate=256)

    if success and os.path.exists(final_mp3_path):
        print(f"[SUCCESS] Successfully generated: {final_mp3_path}")
        verify_audio_quality(final_mp3_path)
        return True
    else:
        print(f"[ERROR] Post-processing failed for Chapter {ch_str}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_bilingual_audio.py <chapter_number: 1..27 or all> [ko_engine: edge|qwen]")
        sys.exit(1)

    arg = sys.argv[1].lower()
    ko_engine = sys.argv[2].lower() if len(sys.argv) > 2 else "edge"

    if arg == "all":
        for ch in range(1, 28):
            generate_bilingual_chapter(ch, ko_engine=ko_engine)
    else:
        try:
            ch_num = int(arg)
            generate_bilingual_chapter(ch_num, ko_engine=ko_engine)
        except ValueError:
            print("Invalid chapter number. Specify integer (1..27) or 'all'.")
            sys.exit(1)

if __name__ == "__main__":
    main()
